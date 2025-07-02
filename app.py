from flask import Flask, jsonify, request
import json
import uuid
from datetime import datetime

app = Flask(__name__)

# AGENT_CARD 정보
AGENT_CARD = {
    "name": "A2A Agent",
    "version": "1.0.0",
    "description": "Simple A2A agent server",
    "capabilities": [
        "text_processing",
        "data_analysis",
        "general_tasks"
    ],
    "endpoints": {
        "jsonrpc": "/jsonrpc"
    }
}

@app.route('/agent-card.json', methods=['GET'])
def get_agent_card():
    """AGENT_CARD 정보를 반환"""
    return jsonify(AGENT_CARD)

@app.route('/jsonrpc', methods=['POST'])
def jsonrpc_handler():
    """JSON-RPC 요청을 처리하는 엔드포인트"""
    try:
        # 요청 데이터 파싱
        data = request.get_json()
        
        # JSON-RPC 기본 검증
        if not data or 'method' not in data:
            return create_error_response(-32600, "Invalid Request", None)
        
        method = data.get('method')
        params = data.get('params', {})
        request_id = data.get('id')
        
        # 메소드에 따른 작업 처리
        if method == 'process_task':
            result = process_task(params)
        elif method == 'analyze_data':
            result = analyze_data(params)
        elif method == 'generate_text':
            result = generate_text(params)
        else:
            return create_error_response(-32601, "Method not found", request_id)
        
        # 성공 응답 생성
        response = {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }
        
        return jsonify(response)
    
    except Exception as e:
        return create_error_response(-32603, f"Internal error: {str(e)}", request_id)

def create_error_response(code, message, request_id):
    """에러 응답 생성"""
    return jsonify({
        "jsonrpc": "2.0",
        "error": {
            "code": code,
            "message": message
        },
        "id": request_id
    }), 400

def process_task(params):
    """일반 작업 처리"""
    task = params.get('task', 'default task')
    
    # 간단한 작업 처리 로직
    result_data = f"Processed task: {task}"
    
    # Artifact 생성
    artifact = create_artifact("task_result", "text", result_data)
    
    return {
        "status": "completed",
        "message": "Task processed successfully",
        "artifact": artifact,
        "timestamp": datetime.now().isoformat()
    }

def analyze_data(params):
    """데이터 분석 작업"""
    data = params.get('data', [])
    
    # 간단한 데이터 분석
    if isinstance(data, list) and data:
        analysis = {
            "count": len(data),
            "sample": data[:3] if len(data) > 3 else data,
            "summary": f"Analyzed {len(data)} items"
        }
    else:
        analysis = {"message": "No valid data provided"}
    
    # Artifact 생성
    artifact = create_artifact("analysis_result", "json", analysis)
    
    return {
        "status": "completed",
        "analysis": analysis,
        "artifact": artifact,
        "timestamp": datetime.now().isoformat()
    }

def generate_text(params):
    """텍스트 생성 작업"""
    prompt = params.get('prompt', 'Hello')
    length = params.get('length', 50)
    
    # 간단한 텍스트 생성 (실제로는 더 복잡한 로직 필요)
    generated_text = f"Generated response for '{prompt}': " + "This is a sample generated text. " * (length // 20 + 1)
    generated_text = generated_text[:length]
    
    # Artifact 생성
    artifact = create_artifact("generated_text", "text", generated_text)
    
    return {
        "status": "completed",
        "text": generated_text,
        "artifact": artifact,
        "timestamp": datetime.now().isoformat()
    }

def create_artifact(name, artifact_type, content):
    """Artifact 생성 헬퍼 함수"""
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "type": artifact_type,
        "content": content,
        "created_at": datetime.now().isoformat(),
        "size": len(str(content)) if content else 0
    }

if __name__ == '__main__':
    print("Starting A2A Server...")
    print("Available endpoints:")
    print("- GET /agent-card.json")
    print("- POST /jsonrpc")
    print("\nSupported methods:")
    print("- process_task")
    print("- analyze_data") 
    print("- generate_text")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
