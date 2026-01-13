"""
Web interface for Revamp Agent using FastAPI.
Makes the tool accessible to non-technical users through a browser.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
import uuid
from datetime import datetime

try:
    from app.main import revamp_project, revamp_and_implement
    from app.session_manager import get_session_manager, SessionStatus
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.main import revamp_project, revamp_and_implement
    from app.session_manager import get_session_manager, SessionStatus

app = FastAPI(
    title="Revamp Agent Web Interface",
    description="Transform GitHub projects into hackathon winners",
    version="1.0.0"
)

# Session manager
session_manager = get_session_manager()

# In-memory job storage (use Redis in production)
jobs = {}

class RevampRequest(BaseModel):
    github_url: Optional[str] = None
    hackathon_url: Optional[str] = None
    hackathon_context: Optional[str] = None
    search_topic: Optional[str] = None
    search_order: str = "projects_first"
    implement_changes: bool = False
    fork_repo: bool = False
    branch_name: str = "hackathon-revamp"

class JobStatus(BaseModel):
    job_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: int  # 0-100
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: str
    updated_at: str

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main web interface."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Revamp Agent - Transform Projects into Hackathon Winners</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 10px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: 500; color: #333; }
            input, textarea, select { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
            textarea { height: 80px; resize: vertical; }
            .checkbox-group { display: flex; align-items: center; gap: 10px; }
            .checkbox-group input { width: auto; }
            button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; width: 100%; }
            button:hover { background: #0056b3; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; border-left: 4px solid #007bff; }
            .error { border-left-color: #dc3545; background: #f8d7da; }
            .loading { text-align: center; padding: 20px; }
            .progress { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin: 10px 0; }
            .progress-bar { height: 100%; background: #007bff; transition: width 0.3s ease; }
            .tabs { display: flex; margin-bottom: 20px; border-bottom: 1px solid #ddd; }
            .tab { padding: 10px 20px; cursor: pointer; border-bottom: 2px solid transparent; }
            .tab.active { border-bottom-color: #007bff; color: #007bff; }
            .tab-content { display: none; }
            .tab-content.active { display: block; }
            .example-links { margin: 20px 0; padding: 15px; background: #e7f3ff; border-radius: 5px; }
            .example-links a { color: #007bff; text-decoration: none; margin-right: 15px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Revamp Agent</h1>
            <p class="subtitle">Transform GitHub projects into hackathon winners with AI</p>
            
            <div class="tabs">
                <div class="tab active" onclick="switchTab('simple')">Simple Mode</div>
                <div class="tab" onclick="switchTab('advanced')">Advanced Mode</div>
                <div class="tab" onclick="switchTab('discovery')">Discovery Mode</div>
            </div>
            
            <!-- Simple Mode -->
            <div id="simple" class="tab-content active">
                <form id="simpleForm">
                    <div class="form-group">
                        <label for="github_url">GitHub Repository URL</label>
                        <input type="url" id="github_url" name="github_url" placeholder="https://github.com/user/repo">
                    </div>
                    
                    <div class="form-group">
                        <label for="hackathon_url">Hackathon Website URL</label>
                        <input type="url" id="hackathon_url" name="hackathon_url" placeholder="https://hackathon-website.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="hackathon_context">Additional Context (Optional)</label>
                        <textarea id="hackathon_context" name="hackathon_context" placeholder="Describe the hackathon theme, requirements, or any specific details..."></textarea>
                    </div>
                    
                    <button type="submit">Generate Strategy</button>
                </form>
            </div>
            
            <!-- Advanced Mode -->
            <div id="advanced" class="tab-content">
                <form id="advancedForm">
                    <div class="form-group">
                        <label for="adv_github_url">GitHub Repository URL</label>
                        <input type="url" id="adv_github_url" name="github_url" placeholder="https://github.com/user/repo">
                    </div>
                    
                    <div class="form-group">
                        <label for="adv_hackathon_url">Hackathon Website URL</label>
                        <input type="url" id="adv_hackathon_url" name="hackathon_url" placeholder="https://hackathon-website.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="adv_hackathon_context">Additional Context</label>
                        <textarea id="adv_hackathon_context" name="hackathon_context" placeholder="Hackathon details..."></textarea>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="implement_changes" name="implement_changes">
                        <label for="implement_changes">Implement code changes automatically</label>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="fork_repo" name="fork_repo">
                        <label for="fork_repo">Fork repository before making changes</label>
                    </div>
                    
                    <div class="form-group">
                        <label for="branch_name">Branch Name</label>
                        <input type="text" id="branch_name" name="branch_name" value="hackathon-revamp">
                    </div>
                    
                    <button type="submit">Generate & Implement</button>
                </form>
            </div>
            
            <!-- Discovery Mode -->
            <div id="discovery" class="tab-content">
                <form id="discoveryForm">
                    <div class="form-group">
                        <label for="search_topic">Search Topic</label>
                        <input type="text" id="search_topic" name="search_topic" placeholder="e.g., AI, web3, climate, healthcare">
                    </div>
                    
                    <div class="form-group">
                        <label for="search_order">Discovery Order</label>
                        <select id="search_order" name="search_order">
                            <option value="projects_first">Find Projects First</option>
                            <option value="hackathons_first">Find Hackathons First</option>
                        </select>
                    </div>
                    
                    <div class="checkbox-group">
                        <input type="checkbox" id="disc_implement_changes" name="implement_changes">
                        <label for="disc_implement_changes">Implement code changes</label>
                    </div>
                    
                    <button type="submit">Discover & Revamp</button>
                </form>
                
                <div class="example-links">
                    <strong>Try these topics:</strong>
                    <a href="#" onclick="setTopic('AI')">AI</a>
                    <a href="#" onclick="setTopic('web3')">Web3</a>
                    <a href="#" onclick="setTopic('climate')">Climate</a>
                    <a href="#" onclick="setTopic('healthcare')">Healthcare</a>
                </div>
            </div>
            
            <div id="result"></div>
        </div>
        
        <script>
            let currentJobId = null;
            
            function switchTab(tabName) {
                // Hide all tabs
                document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
                document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
                
                // Show selected tab
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }
            
            function setTopic(topic) {
                document.getElementById('search_topic').value = topic;
            }
            
            async function submitForm(formData, endpoint) {
                const resultDiv = document.getElementById('result');
                resultDiv.innerHTML = '<div class="loading">🚀 Starting revamp process...</div>';
                
                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(formData)
                    });
                    
                    const job = await response.json();
                    currentJobId = job.job_id;
                    
                    // Poll for results
                    pollJobStatus(job.job_id);
                    
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">❌ Error: ${error.message}</div>`;
                }
            }
            
            async function pollJobStatus(jobId) {
                const resultDiv = document.getElementById('result');
                
                try {
                    const response = await fetch(`/jobs/${jobId}`);
                    const job = await response.json();
                    
                    // Update progress
                    resultDiv.innerHTML = `
                        <div class="loading">
                            <div>Status: ${job.status}</div>
                            <div class="progress">
                                <div class="progress-bar" style="width: ${job.progress}%"></div>
                            </div>
                            <div>${job.progress}% complete</div>
                        </div>
                    `;
                    
                    if (job.status === 'completed') {
                        resultDiv.innerHTML = `
                            <div class="result">
                                <h3>✅ Revamp Complete!</h3>
                                <pre>${JSON.stringify(job.result, null, 2)}</pre>
                            </div>
                        `;
                    } else if (job.status === 'failed') {
                        resultDiv.innerHTML = `
                            <div class="result error">
                                <h3>❌ Revamp Failed</h3>
                                <p>${job.error}</p>
                            </div>
                        `;
                    } else {
                        // Continue polling
                        setTimeout(() => pollJobStatus(jobId), 2000);
                    }
                    
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">❌ Error checking status: ${error.message}</div>`;
                }
            }
            
            // Form handlers
            document.getElementById('simpleForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = Object.fromEntries(new FormData(e.target));
                await submitForm(formData, '/revamp');
            });
            
            document.getElementById('advancedForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = Object.fromEntries(new FormData(e.target));
                formData.implement_changes = document.getElementById('implement_changes').checked;
                formData.fork_repo = document.getElementById('fork_repo').checked;
                await submitForm(formData, '/revamp');
            });
            
            document.getElementById('discoveryForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const formData = Object.fromEntries(new FormData(e.target));
                formData.implement_changes = document.getElementById('disc_implement_changes').checked;
                await submitForm(formData, '/revamp');
            });
        </script>
    </body>
    </html>
    """

@app.post("/revamp")
async def create_revamp_job(request: RevampRequest, background_tasks: BackgroundTasks):
    """Create a new revamp job."""
    job_id = str(uuid.uuid4())
    
    # Create job entry
    jobs[job_id] = JobStatus(
        job_id=job_id,
        status="pending",
        progress=0,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    # Start background task
    background_tasks.add_task(run_revamp_job, job_id, request)
    
    return {"job_id": job_id, "status": "pending"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status and results."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return jobs[job_id]

async def run_revamp_job(job_id: str, request: RevampRequest):
    """Run the revamp job in the background."""
    try:
        # Update status
        jobs[job_id].status = "running"
        jobs[job_id].progress = 10
        jobs[job_id].updated_at = datetime.now().isoformat()
        
        # Run the revamp
        if request.implement_changes:
            jobs[job_id].progress = 30
            result = revamp_and_implement(
                github_url=request.github_url,
                hackathon_url=request.hackathon_url,
                hackathon_context=request.hackathon_context,
                search_order=request.search_order,
                search_topic=request.search_topic,
                implement_changes=request.implement_changes,
                fork_repo=request.fork_repo,
                branch_name=request.branch_name
            )
        else:
            jobs[job_id].progress = 50
            result = revamp_project(
                github_url=request.github_url,
                hackathon_url=request.hackathon_url,
                hackathon_context=request.hackathon_context,
                search_order=request.search_order,
                search_topic=request.search_topic
            )
        
        # Complete job
        jobs[job_id].status = "completed"
        jobs[job_id].progress = 100
        jobs[job_id].result = result if isinstance(result, dict) else {"strategy": result}
        jobs[job_id].updated_at = datetime.now().isoformat()
        
    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)
        jobs[job_id].updated_at = datetime.now().isoformat()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)