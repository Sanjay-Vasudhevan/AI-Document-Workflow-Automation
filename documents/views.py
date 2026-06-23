import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from pypdf import PdfReader
from google import genai
from google.genai import types

from .models import Document
from .forms import DocumentUploadForm

def extract_text_from_file(file_path):
    """Extracts raw text content from an uploaded document."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    try:
        if ext == '.pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read(10000)
    except Exception as e:
        print(f"Extraction Error: {e}")
        
    return text.strip()

def analyze_document_with_ai(document):
    """Passes text context to Gemini and updates model database metrics."""
    file_path = document.file.path
    extracted_text = extract_text_from_file(file_path)
    
    if not extracted_text:
        document.ai_summary = "Failed to extract readable text content from this file structure."
        document.ai_category = "Unknown"
        document.ai_priority = "Medium"
        document.save()
        return

    # Prompt constructing a structured JSON reply format requirement
    prompt = f"""
    Analyze the following extracted document text. Provide your response in a strict raw JSON format containing exactly three keys: "summary", "category", and "priority".
    
    - "summary": A concise 2-3 sentence overview of the document's main content.
    - "category": Classify this document type (e.g., Resume, Invoice, Project Proposal, Report, Contract).
    - "priority": Assign a priority tier based on potential urgency (High, Medium, Low).

    Document Text Content:
    \"\"\"{extracted_text[:4000]}\"\"\"
    """

    try:
        # Pull the key securely from settings
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        
        # Initialize the client by passing the token explicitly through the Client configuration
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            ),
        )
        
        # Parse output data clean from structured text token response block
        data = json.loads(response.text.strip())
        
        document.ai_summary = data.get('summary', 'No summary generated.')
        document.ai_category = data.get('category', 'Uncategorized')
        document.ai_priority = data.get('priority', 'Medium')
        document.save()
        
    except Exception as e:
        print(f"Gemini API Engine Crash Exception: {e}")
        document.ai_summary = f"AI model error encountered processing document: {str(e)}"
        document.ai_category = "Error Logged"
        document.ai_priority = "High"
        document.save()

@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            
            # Fire processing engine pipeline sync hook right here
            analyze_document_with_ai(document)
            
            messages.success(request, f"Document '{document.title}' uploaded and analyzed by AI successfully!")
            return redirect('document_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'documents/document_upload.html', {'form': form})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})

@login_required
def review_document(request, pk):
    """Processes manager approval/rejection decisions and manual text remarks."""
    # FIXED: Check for staff status or superuser access to validate permissions seamlessly
    if not request.user.is_staff and not request.user.is_superuser:
        messages.error(request, "Access Denied: You do not have Manager permissions.")
        return redirect('document_list')

    if request.method == 'POST':
        document = get_object_or_404(Document, pk=pk)
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '').strip()

        if action == 'APPROVE':
            document.status = 'APPROVED'
            messages.success(request, f"Document '{document.title}' has been APPROVED.")
        elif action == 'DECLINE':
            document.status = 'REJECTED'
            messages.warning(request, f"Document '{document.title}' has been REJECTED.")

        document.manager_remarks = remarks
        document.save()

    return redirect('document_detail', pk=pk)