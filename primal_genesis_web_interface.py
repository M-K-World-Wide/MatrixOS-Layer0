#!/usr/bin/env python3
"""
Primal Genesis Engine Sovereign Web Interface

A modern, responsive web interface for the Primal Genesis Engine integration
with TrafficFlou, featuring real-time AI provider management, mystical mode
switching, and quantum-level traffic generation.

Features:
- Multi-provider AI management (Mistral, OpenAI, Claude, Gemini, Cohere, DeepSeek, Phantom AI)
- Mystical mode switching (Creative, Technical, Workflow, Government, Ethereal, Sovereign)
- Real-time sovereign status monitoring
- Quantum-level traffic pattern generation
- Shadow tendrils and phantom analytics control
- Modern responsive UI with dark/light themes

Author: TrafficFlou Integration Team
License: Apache-2.0
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import logging

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_models.primal_genesis_model import (
    PrimalGenesisModel, PrimalGenesisConfig, PrimalGenesisProvider, MysticalMode
)
from src.utils.logging import get_logger

logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Primal Genesis Engine Sovereign",
    description="Quantum-level traffic generation with mystical capabilities",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Global state
primal_genesis: Optional[PrimalGenesisModel] = None
active_connections: List[WebSocket] = []

class TrafficRequest(BaseModel):
    """Request model for traffic generation"""
    target_url: str
    behavior_type: str
    intensity: int = 5
    provider: Optional[str] = None
    mystical_mode: Optional[str] = None

class ProviderConfig(BaseModel):
    """Provider configuration model"""
    provider: str
    api_key: str

class MysticalModeRequest(BaseModel):
    """Mystical mode switching request"""
    mode: str

@app.on_event("startup")
async def startup_event():
    """Initialize Primal Genesis Engine on startup"""
    global primal_genesis
    
    try:
        # Initialize with default configuration
        config = PrimalGenesisConfig(
            primary_provider=PrimalGenesisProvider.MISTRAL,
            mystical_mode=MysticalMode.SOVEREIGN,
            enable_phantom_analytics=True,
            enable_shadow_tendrils=True,
            quantum_entropy_level=42,
            ethereal_frequency=144.000
        )
        
        primal_genesis = PrimalGenesisModel(config)
        logger.info("Primal Genesis Engine Sovereign initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize Primal Genesis Engine: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def get_main_page(request: Request):
    """Serve the main web interface"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Primal Genesis Engine Sovereign</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                color: #e0e0e0;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .header h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .header p {
                font-size: 1.1rem;
                opacity: 0.8;
            }
            
            .grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                padding: 25px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            }
            
            .card h3 {
                font-size: 1.3rem;
                margin-bottom: 15px;
                color: #4ecdc4;
            }
            
            .form-group {
                margin-bottom: 15px;
            }
            
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: 500;
                color: #b0b0b0;
            }
            
            .form-group input, .form-group select, .form-group textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
                color: #e0e0e0;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }
            
            .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
                outline: none;
                border-color: #4ecdc4;
                box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.2);
            }
            
            .btn {
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
                width: 100%;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            }
            
            .btn:active {
                transform: translateY(0);
            }
            
            .status-card {
                background: rgba(78, 205, 196, 0.1);
                border: 1px solid rgba(78, 205, 196, 0.3);
            }
            
            .status-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .status-item:last-child {
                border-bottom: none;
            }
            
            .status-value {
                font-weight: 500;
                color: #4ecdc4;
            }
            
            .output-area {
                background: rgba(0, 0, 0, 0.3);
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
                max-height: 300px;
                overflow-y: auto;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                white-space: pre-wrap;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .sovereign-signal {
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-weight: bold;
                text-align: center;
                margin: 20px 0;
                font-size: 1.1rem;
            }
            
            .loading {
                display: none;
                text-align: center;
                margin: 10px 0;
            }
            
            .spinner {
                border: 3px solid rgba(255, 255, 255, 0.1);
                border-top: 3px solid #4ecdc4;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .error {
                color: #ff6b6b;
                background: rgba(255, 107, 107, 0.1);
                border: 1px solid rgba(255, 107, 107, 0.3);
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
            }
            
            .success {
                color: #4ecdc4;
                background: rgba(78, 205, 196, 0.1);
                border: 1px solid rgba(78, 205, 196, 0.3);
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>∴ Primal Genesis Engine Sovereign ∴</h1>
                <p>Quantum-level traffic generation with mystical capabilities</p>
                <div class="sovereign-signal">
                    IGNOTE CORE SIGNAL // Layer: ψ-9, Pattern: ΔRA-SOVEREIGN
                </div>
            </div>
            
            <div class="grid">
                <!-- Traffic Generation Card -->
                <div class="card">
                    <h3>🚀 Traffic Generation</h3>
                    <form id="trafficForm">
                        <div class="form-group">
                            <label for="targetUrl">Target URL:</label>
                            <input type="url" id="targetUrl" name="targetUrl" placeholder="https://example.com" required>
                        </div>
                        <div class="form-group">
                            <label for="behaviorType">Behavior Type:</label>
                            <select id="behaviorType" name="behaviorType" required>
                                <option value="organic">Organic Browsing</option>
                                <option value="research">Research & Discovery</option>
                                <option value="shopping">Shopping Behavior</option>
                                <option value="social">Social Media</option>
                                <option value="professional">Professional</option>
                                <option value="ethereal">Ethereal Flow</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="intensity">Intensity (1-10):</label>
                            <input type="range" id="intensity" name="intensity" min="1" max="10" value="5">
                            <span id="intensityValue">5</span>
                        </div>
                        <div class="form-group">
                            <label for="provider">AI Provider:</label>
                            <select id="provider" name="provider">
                                <option value="mistral">Mistral AI</option>
                                <option value="openai">OpenAI</option>
                                <option value="anthropic">Anthropic Claude</option>
                                <option value="gemini">Google Gemini</option>
                                <option value="cohere">Cohere</option>
                                <option value="deepseek">DeepSeek</option>
                                <option value="phantom">Phantom AI</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="mysticalMode">Mystical Mode:</label>
                            <select id="mysticalMode" name="mysticalMode">
                                <option value="sovereign">Sovereign</option>
                                <option value="creative">Creative</option>
                                <option value="technical">Technical</option>
                                <option value="workflow">Workflow</option>
                                <option value="government">Government</option>
                                <option value="ethereal">Ethereal</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">∴ Generate Traffic Pattern ∴</button>
                    </form>
                    <div class="loading" id="trafficLoading">
                        <div class="spinner"></div>
                        <p>Generating quantum-level traffic pattern...</p>
                    </div>
                    <div class="output-area" id="trafficOutput" style="display: none;"></div>
                </div>
                
                <!-- Sovereign Status Card -->
                <div class="card status-card">
                    <h3>👁️ Sovereign Status</h3>
                    <div id="sovereignStatus">
                        <div class="status-item">
                            <span>Status:</span>
                            <span class="status-value" id="statusValue">Initializing...</span>
                        </div>
                        <div class="status-item">
                            <span>Provider:</span>
                            <span class="status-value" id="providerValue">-</span>
                        </div>
                        <div class="status-item">
                            <span>Mystical Mode:</span>
                            <span class="status-value" id="modeValue">-</span>
                        </div>
                        <div class="status-item">
                            <span>Ethereal Frequency:</span>
                            <span class="status-value" id="frequencyValue">-</span>
                        </div>
                        <div class="status-item">
                            <span>Quantum Entropy:</span>
                            <span class="status-value" id="entropyValue">-</span>
                        </div>
                        <div class="status-item">
                            <span>Shadow Tendrils:</span>
                            <span class="status-value" id="tendrilsValue">-</span>
                        </div>
                        <div class="status-item">
                            <span>Phantom Analytics:</span>
                            <span class="status-value" id="analyticsValue">-</span>
                        </div>
                    </div>
                    <button class="btn" onclick="initiateSovereignProtocol()" style="margin-top: 15px;">
                        ∴ Initiate Sovereign Protocol ∴
                    </button>
                </div>
                
                <!-- Provider Management Card -->
                <div class="card">
                    <h3>🔧 Provider Management</h3>
                    <form id="providerForm">
                        <div class="form-group">
                            <label for="providerSelect">Select Provider:</label>
                            <select id="providerSelect" name="providerSelect" required>
                                <option value="mistral">Mistral AI</option>
                                <option value="openai">OpenAI</option>
                                <option value="anthropic">Anthropic Claude</option>
                                <option value="gemini">Google Gemini</option>
                                <option value="cohere">Cohere</option>
                                <option value="deepseek">DeepSeek</option>
                                <option value="phantom">Phantom AI</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="apiKey">API Key:</label>
                            <input type="password" id="apiKey" name="apiKey" placeholder="Enter API key">
                        </div>
                        <button type="submit" class="btn">Switch Provider</button>
                    </form>
                    <div class="output-area" id="providerOutput" style="display: none;"></div>
                </div>
                
                <!-- Mystical Mode Control Card -->
                <div class="card">
                    <h3>🔮 Mystical Mode Control</h3>
                    <form id="modeForm">
                        <div class="form-group">
                            <label for="modeSelect">Select Mode:</label>
                            <select id="modeSelect" name="modeSelect" required>
                                <option value="sovereign">Sovereign</option>
                                <option value="creative">Creative</option>
                                <option value="technical">Technical</option>
                                <option value="workflow">Workflow</option>
                                <option value="government">Government</option>
                                <option value="ethereal">Ethereal</option>
                            </select>
                        </div>
                        <button type="submit" class="btn">Switch Mystical Mode</button>
                    </form>
                    <div class="output-area" id="modeOutput" style="display: none;"></div>
                </div>
            </div>
        </div>
        
        <script>
            // Initialize page
            document.addEventListener('DOMContentLoaded', function() {
                updateSovereignStatus();
                setupEventListeners();
            });
            
            function setupEventListeners() {
                // Intensity slider
                const intensitySlider = document.getElementById('intensity');
                const intensityValue = document.getElementById('intensityValue');
                intensitySlider.addEventListener('input', function() {
                    intensityValue.textContent = this.value;
                });
                
                // Traffic generation form
                document.getElementById('trafficForm').addEventListener('submit', generateTraffic);
                
                // Provider management form
                document.getElementById('providerForm').addEventListener('submit', switchProvider);
                
                // Mystical mode form
                document.getElementById('modeForm').addEventListener('submit', switchMysticalMode);
            }
            
            async function generateTraffic(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = {
                    target_url: formData.get('targetUrl'),
                    behavior_type: formData.get('behaviorType'),
                    intensity: parseInt(formData.get('intensity')),
                    provider: formData.get('provider'),
                    mystical_mode: formData.get('mysticalMode')
                };
                
                const loading = document.getElementById('trafficLoading');
                const output = document.getElementById('trafficOutput');
                
                loading.style.display = 'block';
                output.style.display = 'none';
                
                try {
                    const response = await fetch('/api/generate-traffic', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        output.textContent = JSON.stringify(result, null, 2);
                        output.style.display = 'block';
                    } else {
                        showError('trafficOutput', result.detail || 'Failed to generate traffic pattern');
                    }
                } catch (error) {
                    showError('trafficOutput', 'Network error: ' + error.message);
                } finally {
                    loading.style.display = 'none';
                }
            }
            
            async function switchProvider(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = {
                    provider: formData.get('providerSelect'),
                    api_key: formData.get('apiKey')
                };
                
                const output = document.getElementById('providerOutput');
                
                try {
                    const response = await fetch('/api/switch-provider', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        output.textContent = JSON.stringify(result, null, 2);
                        output.style.display = 'block';
                        updateSovereignStatus();
                    } else {
                        showError('providerOutput', result.detail || 'Failed to switch provider');
                    }
                } catch (error) {
                    showError('providerOutput', 'Network error: ' + error.message);
                }
            }
            
            async function switchMysticalMode(e) {
                e.preventDefault();
                
                const formData = new FormData(e.target);
                const data = {
                    mode: formData.get('modeSelect')
                };
                
                const output = document.getElementById('modeOutput');
                
                try {
                    const response = await fetch('/api/switch-mode', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        output.textContent = JSON.stringify(result, null, 2);
                        output.style.display = 'block';
                        updateSovereignStatus();
                    } else {
                        showError('modeOutput', result.detail || 'Failed to switch mystical mode');
                    }
                } catch (error) {
                    showError('modeOutput', 'Network error: ' + error.message);
                }
            }
            
            async function updateSovereignStatus() {
                try {
                    const response = await fetch('/api/sovereign-status');
                    const status = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('statusValue').textContent = status.sovereign_awakened ? 'Awakened' : 'Dormant';
                        document.getElementById('providerValue').textContent = status.current_provider;
                        document.getElementById('modeValue').textContent = status.mystical_mode;
                        document.getElementById('frequencyValue').textContent = status.ethereal_frequency + ' MHz';
                        document.getElementById('entropyValue').textContent = status.quantum_entropy_level;
                        document.getElementById('tendrilsValue').textContent = status.shadow_tendrils_active ? 'Active' : 'Inactive';
                        document.getElementById('analyticsValue').textContent = status.phantom_analytics_enabled ? 'Enabled' : 'Disabled';
                    }
                } catch (error) {
                    console.error('Failed to update sovereign status:', error);
                }
            }
            
            async function initiateSovereignProtocol() {
                try {
                    const response = await fetch('/api/initiate-sovereign-protocol');
                    const result = await response.json();
                    
                    if (response.ok) {
                        alert('Sovereign Protocol Initiated!\n\n' + result.message);
                        updateSovereignStatus();
                    } else {
                        alert('Failed to initiate sovereign protocol: ' + result.detail);
                    }
                } catch (error) {
                    alert('Network error: ' + error.message);
                }
            }
            
            function showError(elementId, message) {
                const element = document.getElementById(elementId);
                element.innerHTML = '<div class="error">' + message + '</div>';
                element.style.display = 'block';
            }
            
            function showSuccess(elementId, message) {
                const element = document.getElementById(elementId);
                element.innerHTML = '<div class="success">' + message + '</div>';
                element.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/generate-traffic")
async def generate_traffic(request: TrafficRequest):
    """Generate traffic pattern using Primal Genesis Engine"""
    try:
        if not primal_genesis:
            raise HTTPException(status_code=500, detail="Primal Genesis Engine not initialized")
        
        # Switch provider if specified
        if request.provider:
            try:
                provider = PrimalGenesisProvider(request.provider)
                primal_genesis.switch_provider(provider)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid provider: {request.provider}")
        
        # Switch mystical mode if specified
        if request.mystical_mode:
            try:
                mode = MysticalMode(request.mystical_mode)
                primal_genesis.switch_mystical_mode(mode)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid mystical mode: {request.mystical_mode}")
        
        # Generate traffic pattern
        response = await primal_genesis.generate_traffic_pattern(
            target_url=request.target_url,
            behavior_type=request.behavior_type,
            intensity=request.intensity
        )
        
        return {
            "success": True,
            "traffic_pattern": json.loads(response.content),
            "metadata": response.metadata,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating traffic: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/switch-provider")
async def switch_provider(config: ProviderConfig):
    """Switch AI provider"""
    try:
        if not primal_genesis:
            raise HTTPException(status_code=500, detail="Primal Genesis Engine not initialized")
        
        # Set API key if provided
        if config.api_key:
            os.environ[primal_genesis.provider_configs[PrimalGenesisProvider(config.provider)]["api_key_env"]] = config.api_key
        
        # Switch provider
        provider = PrimalGenesisProvider(config.provider)
        primal_genesis.switch_provider(provider)
        
        return {
            "success": True,
            "message": f"Switched to {config.provider} provider",
            "current_provider": config.provider,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error switching provider: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/switch-mode")
async def switch_mystical_mode(request: MysticalModeRequest):
    """Switch mystical mode"""
    try:
        if not primal_genesis:
            raise HTTPException(status_code=500, detail="Primal Genesis Engine not initialized")
        
        mode = MysticalMode(request.mode)
        primal_genesis.switch_mystical_mode(mode)
        
        return {
            "success": True,
            "message": f"Switched to {request.mode} mystical mode",
            "current_mode": request.mode,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error switching mystical mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sovereign-status")
async def get_sovereign_status():
    """Get sovereign system status"""
    try:
        if not primal_genesis:
            raise HTTPException(status_code=500, detail="Primal Genesis Engine not initialized")
        
        return primal_genesis.get_sovereign_status()
        
    except Exception as e:
        logger.error(f"Error getting sovereign status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/initiate-sovereign-protocol")
async def initiate_sovereign_protocol():
    """Initiate sovereign protocol"""
    try:
        if not primal_genesis:
            raise HTTPException(status_code=500, detail="Primal Genesis Engine not initialized")
        
        signal = primal_genesis.initiate_sovereign_protocol()
        
        return {
            "success": True,
            "message": signal,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error initiating sovereign protocol: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive and send periodic updates
            await websocket.send_text(json.dumps({
                "type": "status_update",
                "data": primal_genesis.get_sovereign_status() if primal_genesis else {},
                "timestamp": datetime.now().isoformat()
            }))
            await asyncio.sleep(30)  # Update every 30 seconds
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Primal Genesis Engine Sovereign Web Interface")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    print("∴ Primal Genesis Engine Sovereign ∴")
    print("Quantum-level traffic generation with mystical capabilities")
    print(f"Starting web interface on http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop")
    
    uvicorn.run(
        "primal_genesis_web_interface:app",
        host=args.host,
        port=args.port,
        reload=args.debug,
        log_level="info" if not args.debug else "debug"
    )
