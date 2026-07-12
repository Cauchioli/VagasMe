import http.server
import json
import os
import urllib.parse
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JOBS_FILE = os.path.join(BASE_DIR, "jobs_database.json")
CANDIDATES_FILE = os.path.join(BASE_DIR, "candidates_database.json")
APPLICATIONS_FILE = os.path.join(BASE_DIR, "applications_database.json")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings_database.json")

# Initial mock data for Itapetininga jobs
INITIAL_JOBS = [
    {
        "id": "job-cofesa-1",
        "empresa": "COFESA ITAPETININGA",
        "ramo": "Supermercado",
        "vagas": ["JOVEM APRENDIZ", "CAIXA"],
        "beneficios": "Vale-Transporte, Vale-Alimentação/Refeição, Assistência Médica, Recreio Escolar, Seguro de Vida.",
        "salarios": "R$ 1.800 até R$ 2.100",
        "turnos": "Diurno e Noturno",
        "endereco": "R. José de Almeida Carvalho, 1000 - Vila Leonor, Itapetininga - SP, 18210-145",
        "latitude": -23.5937,
        "longitude": -48.0645,
        "imagem": "https://images.unsplash.com/photo-1542838132-92c53300491e?w=500&auto=format&fit=crop&q=60",
        "patrocinado": True,
        "estrela": True,
        "descricao": "Oportunidade para início imediato no Cofesa Itapetininga. Buscamos jovens e profissionais dedicados para atendimento ao cliente no caixa e reposição de mercadorias. Oferecemos plano de carreira e ótimo ambiente de trabalho."
    },
    {
        "id": "job-serraria-2",
        "empresa": "SERRARIA CENTRAL ITAPETININGA",
        "ramo": "Madeireira e Construção",
        "vagas": ["SERRALHEIRO", "AJUDANTE GERAL"],
        "beneficios": "Vale-Transporte, Cesta Básica, Seguro de Vida, Adicional de Insalubridade.",
        "salarios": "R$ 2.200 até R$ 2.800",
        "turnos": "Diurno (07:00 às 17:00)",
        "endereco": "Av. Padre Antônio Brunetti, 450 - Vila Rio Branco, Itapetininga - SP",
        "latitude": -23.5855,
        "longitude": -48.0495,
        "imagem": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122?w=500&auto=format&fit=crop&q=60",
        "patrocinado": False,
        "estrela": False,
        "descricao": "Vaga de serralheiro com experiência em solda MIG/TIG e corte de estruturas metálicas. Desejável curso técnico na área. Ajudante geral para carga, descarga e organização do pátio."
    },
    {
        "id": "job-padaria-3",
        "empresa": "PADARIA REAL VILA APARECIDA",
        "ramo": "Alimentação",
        "vagas": ["COPEIRO", "ATENDENTE", "SUSHIMAN"],
        "beneficios": "Refeição no local, Vale-Transporte, Plano de Saúde Co-participativo.",
        "salarios": "R$ 1.900 até R$ 2.500",
        "turnos": "Tarde e Noite (Escala 6x1)",
        "endereco": "R. Virgílio de Rezende, 1200 - Vila Aparecida, Itapetininga - SP",
        "latitude": -23.5905,
        "longitude": -48.0515,
        "imagem": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60",
        "patrocinado": True,
        "estrela": True,
        "descricao": "Procura-se profissional para preparo de alimentos, higienização e suporte na copa. Vaga para Sushiman com habilidades técnicas na preparação de sushis, sashimis e pratos quentes da culinária japonesa."
    },
    {
        "id": "job-boutique-4",
        "empresa": "BOUTIQUE E MODAS ITAPÊ",
        "ramo": "Comércio Varejista",
        "vagas": ["VENDEDOR", "AUX. ADMINISTRATIVO"],
        "beneficios": "Comissão de vendas, Vale-Transporte, Desconto em produtos.",
        "salarios": "R$ 1.600 + Comissão (Média de R$ 2.400)",
        "turnos": "Horário Comercial",
        "endereco": "R. Saldanha Marinho, 320 - Centro, Itapetininga - SP",
        "latitude": -23.5878,
        "longitude": -48.0572,
        "imagem": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=500&auto=format&fit=crop&q=60",
        "patrocinado": False,
        "estrela": False,
        "descricao": "Atendimento ao cliente, organização da loja física e auxílio no controle de estoque. Auxiliar administrativo para faturamento de notas, conciliação e suporte financeiro."
    }
]


def load_json(filepath, default):
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2, ensure_ascii=False)
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return default


def save_json(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving {filepath}: {e}")


# Initialize databases
load_json(JOBS_FILE, INITIAL_JOBS)
load_json(CANDIDATES_FILE, {"candidates": []})
load_json(APPLICATIONS_FILE, {"applications": []})
load_json(SETTINGS_FILE, {"plus_active": False, "total_clicks": 0})


class VagasHandler(http.server.BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        # API Routes
        if self.path == "/api/vagas":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            jobs = load_json(JOBS_FILE, INITIAL_JOBS)
            self.wfile.write(json.dumps(jobs).encode("utf-8"))

        elif self.path == "/api/settings":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            settings = load_json(SETTINGS_FILE, {"plus_active": False, "total_clicks": 0})
            self.wfile.write(json.dumps(settings).encode("utf-8"))

        elif self.path == "/api/candidates":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            
            candidates_db = load_json(CANDIDATES_FILE, {"candidates": []})
            apps_db = load_json(APPLICATIONS_FILE, {"applications": []})
            jobs_db = load_json(JOBS_FILE, INITIAL_JOBS)
            
            # Enrich candidates list with applications and jobs
            result = []
            jobs_map = {j["id"]: j for j in jobs_db}
            
            for cand in candidates_db.get("candidates", []):
                cand_apps = [a for a in apps_db.get("applications", []) if a["candidate_id"] == cand["id"]]
                cand_enriched = cand.copy()
                cand_enriched["candidaturas"] = []
                for app in cand_apps:
                    job = jobs_map.get(app["job_id"])
                    if job:
                        cand_enriched["candidaturas"].append({
                            "job_id": job["id"],
                            "job_title": ", ".join(job["vagas"]),
                            "empresa": job["empresa"],
                            "stage": app["stage"],
                            "match_score": app["match_score"],
                            "date_applied": app["date_applied"]
                        })
                result.append(cand_enriched)
                
            self.wfile.write(json.dumps(result).encode("utf-8"))

        # Serve static HTML/CSS/JS files
        else:
            clean_path = self.path.split("?")[0]
            if clean_path in ["", "/", "/index.html"]:
                filepath = os.path.join(BASE_DIR, "index.html")
                content_type = "text/html"
            else:
                # Security check to prevent directory traversal
                normalized_path = os.path.normpath(clean_path.lstrip("/"))
                if normalized_path.startswith("..") or os.path.isabs(normalized_path):
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b"Forbidden")
                    return
                filepath = os.path.join(os.path.dirname(BASE_DIR), normalized_path)
                
                # Determine content type
                if filepath.endswith(".css"):
                    content_type = "text/css"
                elif filepath.endswith(".js"):
                    content_type = "application/javascript"
                elif filepath.endswith(".png"):
                    content_type = "image/png"
                elif filepath.endswith(".jpg") or filepath.endswith(".jpeg"):
                    content_type = "image/jpeg"
                elif filepath.endswith(".svg"):
                    content_type = "image/svg+xml"
                else:
                    content_type = "text/plain"

            if os.path.exists(filepath) and os.path.isfile(filepath):
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_cors_headers()
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode("utf-8")) if post_data else {}
        except Exception:
            self.send_response(400)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        # Create Job Route
        if self.path == "/api/vagas":
            jobs = load_json(JOBS_FILE, INITIAL_JOBS)
            new_job = {
                "id": "job-" + str(uuid.uuid4())[:8],
                "empresa": payload.get("empresa", "Empresa Local"),
                "ramo": payload.get("ramo", "Comércio"),
                "vagas": payload.get("vagas", ["Vaga Geral"]),
                "beneficios": payload.get("beneficios", "Vale-Transporte"),
                "salarios": payload.get("salarios", "A combinar"),
                "turnos": payload.get("turnos", "Horário Comercial"),
                "endereco": payload.get("endereco", "Itapetininga - SP"),
                "latitude": float(payload.get("latitude", -23.5916)),
                "longitude": float(payload.get("longitude", -48.0531)),
                "imagem": payload.get("imagem", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500&auto=format&fit=crop&q=60"),
                "patrocinado": bool(payload.get("patrocinado", False)),
                "estrela": False,
                "descricao": payload.get("descricao", "")
            }
            jobs.append(new_job)
            save_json(JOBS_FILE, jobs)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(new_job).encode("utf-8"))

        # Save/Register Candidate Resume
        elif self.path == "/api/candidates":
            db = load_json(CANDIDATES_FILE, {"candidates": []})
            candidates = db.setdefault("candidates", [])
            
            cand_id = payload.get("id")
            if not cand_id:
                cand_id = "cand-" + str(uuid.uuid4())[:8]
                payload["id"] = cand_id
                
            found = False
            for i, c in enumerate(candidates):
                if c["id"] == cand_id:
                    candidates[i] = payload
                    found = True
                    break
            if not found:
                candidates.append(payload)
                
            save_json(CANDIDATES_FILE, db)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))

        # Apply for Job
        elif self.path == "/api/candidatar":
            db = load_json(APPLICATIONS_FILE, {"applications": []})
            apps = db.setdefault("applications", [])
            
            candidate_id = payload.get("candidate_id")
            job_id = payload.get("job_id")
            
            if not candidate_id or not job_id:
                self.send_response(400)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b"Missing candidate_id or job_id")
                return

            # Simulate IA Match Score (e.g. 70% to 98% based on match heuristics)
            # Simple keyword overlap between candidate skills and job tags
            cand_db = load_json(CANDIDATES_FILE, {"candidates": []})
            cand = next((c for c in cand_db.get("candidates", []) if c["id"] == candidate_id), None)
            match_score = 75 # Default fallback
            
            if cand:
                skills_str = " ".join(cand.get("skills", [])).lower()
                jobs_db = load_json(JOBS_FILE, INITIAL_JOBS)
                job = next((j for j in jobs_db if j["id"] == job_id), None)
                if job:
                    overlap_count = 0
                    job_keywords = [w.lower() for w in job["vagas"] + [job["ramo"]] + job["descricao"].split()]
                    for kw in job_keywords:
                        if len(kw) > 3 and kw in skills_str:
                            overlap_count += 1
                    match_score = min(98, 70 + (overlap_count * 4))

            new_app = {
                "id": "app-" + str(uuid.uuid4())[:8],
                "candidate_id": candidate_id,
                "job_id": job_id,
                "stage": "applied", # applied, triagem, entrevista, proposta, rejeitado
                "match_score": match_score,
                "date_applied": datetime.now().isoformat()
            }
            
            # Prevent double application
            exists = next((a for a in apps if a["candidate_id"] == candidate_id and a["job_id"] == job_id), None)
            if exists:
                new_app = exists
            else:
                apps.append(new_app)
                save_json(APPLICATIONS_FILE, db)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(new_app).encode("utf-8"))

        # Update candidate Kanban Stage
        elif self.path == "/api/candidates/update-stage":
            db = load_json(APPLICATIONS_FILE, {"applications": []})
            apps = db.setdefault("applications", [])
            
            candidate_id = payload.get("candidate_id")
            job_id = payload.get("job_id")
            new_stage = payload.get("stage")
            
            found = False
            for a in apps:
                if a["candidate_id"] == candidate_id and a["job_id"] == job_id:
                    a["stage"] = new_stage
                    found = True
                    break
            
            if found:
                save_json(APPLICATIONS_FILE, db)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            else:
                self.send_response(404)
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(b"Application not found")

        # Toggle/Activate Plus Subscription Settings
        elif self.path == "/api/settings/toggle-plus":
            settings = load_json(SETTINGS_FILE, {"plus_active": False, "total_clicks": 0})
            settings["plus_active"] = not settings["plus_active"]
            save_json(SETTINGS_FILE, settings)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps(settings).encode("utf-8"))

        # AI Mock Help: Job Description Generator
        elif self.path == "/api/ia/descricao":
            titulo = payload.get("titulo", "Atendente")
            ramo = payload.get("ramo", "Comércio")
            
            # Simple AI prompt generator template
            descricao_gerada = (
                f"Buscamos um(a) profissional dedicado(a) para atuar como {titulo} em nossa equipe de {ramo}.\n\n"
                f"Principais responsabilidades:\n"
                f"- Atendimento direto ao cliente e suporte às rotinas do setor.\n"
                f"- Organização da área de trabalho e conferência de materiais/produtos.\n"
                f"- Colaboração contínua com a gerência para otimização do fluxo diário.\n\n"
                f"Requisitos:\n"
                f"- Boa comunicação interpessoal e foco na solução de problemas.\n"
                f"- Organização, pontualidade e proatividade.\n"
                f"- Residir preferencialmente em Itapetininga/SP."
            )
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"descricao": descricao_gerada}).encode("utf-8"))

        # AI Mock Help: Resume Optimizer
        elif self.path == "/api/ia/otimizar-curriculo":
            resumo = payload.get("resumo", "")
            habilidades = payload.get("habilidades", [])
            
            otimizado = (
                f"{resumo} Profissional com perfil proativo, focado no aprimoramento de processos e "
                f"entrega de resultados rápidos. Especialista em {', '.join(habilidades[:3])}."
            )
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"otimizado": otimizado}).encode("utf-8"))

        else:
            self.send_response(404)
            self.send_cors_headers()
            self.end_headers()


def run():
    server_class = http.server.HTTPServer
    if hasattr(http.server, "ThreadingHTTPServer"):
        server_class = http.server.ThreadingHTTPServer
        
    with server_class(("", 5000), VagasHandler) as httpd:
        print("Server Vagas.me running at http://localhost:5000")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")


if __name__ == "__main__":
    run()
