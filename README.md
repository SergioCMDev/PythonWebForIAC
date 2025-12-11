# Python Web Application for IaC Deployments

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Descripción

Aplicación web Python minimalista diseñada específicamente para ser desplegada mediante **Infraestructura como Código (IaC)**. 
Este proyecto sirve como aplicación de demostración para pipelines CI/CD, despliegues Blue-Green en Kubernetes, y prácticas DevOps en entornos cloud.

Se integra con [Infra-AWS-EKS-Python](https://github.com/SergioCMDev/Infra-AWS-EKS-Python) y demostraciones de automatización de infraestructura con Terraform y GitHub Actions.

## Características

-  **Aplicación Ligera**: Footprint mínimo, ideal para demos y testing rápido
-  **Docker Native**: Containerizada y lista para Kubernetes
-  **CI/CD Integrado**: Pipeline automatizado con GitHub Actions
-  **Info de Deployment**: Muestra versión, entorno y metadata en tiempo real
-  **UI Simple**: Interfaz limpia que facilita verificar despliegues
-  **Arranque Rápido**: De código a contenedor en segundos

##  Arquitectura

```
┌─────────────────────────────────────────────┐
│         Python Web Application              │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │          app.py                    │    │
│  │                                     │    │
│  │  • Flask Web Server                │    │
│  │  • Environment Variables           │    │
│  │  • Version Display                 │    │
│  │  • Health Endpoints                │    │
│  └────────────────────────────────────┘    │
│                                              │
│  ┌────────────────────────────────────┐    │
│  │      requirements.txt              │    │
│  │  • Flask                            │    │
│  │  • Gunicorn (production)           │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │    Dockerfile          │
        │  Multi-stage build     │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Container Runtime     │
        │  Docker / Kubernetes   │
        └────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   GitHub Actions       │
        │  Build & Deploy        │
        └────────────────────────┘
```

##  Stack Tecnológico

### Backend
- **Python 3.x** - Lenguaje principal
- **Flask** - Framework web minimalista
- **Gunicorn** - WSGI HTTP Server para producción

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación local
- **GitHub Actions** - CI/CD automatizado
- **Kubernetes** - Orquestación (target deployment)

## Estructura del Proyecto

```
.
├── .github/
│   └── workflows/
│       ├── build.yml              # Pipeline de build
│       └── deploy.yml             # Pipeline de despliegue
│
├── app.py                         # Aplicación Flask principal
├── requirements.txt               # Dependencias Python
├── Dockerfile                     # Imagen Docker multi-stage
├── compose.yml                    # Docker Compose para desarrollo
├── .dockerignore                  # Archivos excluidos del build
└── README.md                      # Este archivo
```

## Pre-requisitos

### Para Desarrollo Local
- Python 3.8 o superior
- pip (gestor de paquetes Python)

### Para Despliegue con Docker
- Docker 20.10+
- Docker Compose 2.0+ (opcional)

### Para CI/CD
- Cuenta de GitHub
- Registro de contenedores (Docker Hub, ECR, etc.)

## Instalación y Configuración

### Opción 1: Desarrollo Local

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/SergioCMDev/PythonWebForIAC.git
cd PythonWebForIAC
```

#### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 3. Ejecutar la Aplicación
```bash
python app.py
```

La aplicación estará disponible en `http://localhost:5000`

### Opción 2: Con Docker

#### 1. Construir la Imagen
```bash
docker build -t python-web-iac:latest .
```

#### 2. Ejecutar el Contenedor
```bash
docker run -d \
  --name python-web \
  -p 5000:5000 \
  -e APP_VERSION=1.0.0 \
  -e ENVIRONMENT=production \
  python-web-iac:latest
```

#### 3. Verificar el Contenedor
```bash
docker ps
docker logs python-web
curl http://localhost:5000
```

### Opción 3: Con Docker Compose

#### 1. Levantar Servicios
```bash
docker-compose up -d
```

#### 2. Ver Logs
```bash
docker-compose logs -f
```

#### 3. Detener Servicios
```bash
docker-compose down
```

## Endpoints Disponibles

### Principales

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página principal con info de deployment |
| `/health` | GET | Health check (200 OK) |
| `/version` | GET | Versión de la aplicación |
| `/env` | GET | Variables de entorno (dev only) |

### Ejemplos de Uso

**Verificar la aplicación:**
```bash
curl http://localhost:5000
```

**Health check:**
```bash
curl http://localhost:5000/health
# Response: {"status": "healthy", "timestamp": "2024-12-11T10:30:00Z"}
```

**Ver versión:**
```bash
curl http://localhost:5000/version
# Response: {"version": "1.0.0", "environment": "production"}
```

##  Docker

### Dockerfile Optimizado

El Dockerfile implementa un build multi-stage para optimizar el tamaño de la imagen:

```dockerfile
# Stage 1: Builder
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY app.py .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]
```

### Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `APP_VERSION` | Versión de la aplicación | 1.0.0 |
| `ENVIRONMENT` | Entorno (dev/staging/prod) | development |
| `PORT` | Puerto de escucha | 5000 |

## CI/CD con GitHub Actions

### Pipeline Automatizado

El repositorio incluye workflows de GitHub Actions para automatizar el build y despliegue:

```yaml
# .github/workflows/build.yml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker Image
        run: docker build -t python-web:${{ github.sha }} .
      
      - name: Tag Latest
        run: docker tag python-web:${{ github.sha }} python-web:latest
      
      - name: Push to Registry
        run: docker push python-web:latest
```

### Integración con EKS

Esta aplicación está diseñada para desplegarse en el cluster EKS creado por [Infra-AWS-EKS-Python](https://github.com/SergioCMDev/Infra-AWS-EKS-Python):

```bash
# 1. Build y push de la imagen
docker build -t <ECR_REPO>/python-web:v1.0 .
docker push <ECR_REPO>/python-web:v1.0

# 2. Deploy a Kubernetes
kubectl set image deployment/python-app \
  python-app=<ECR_REPO>/python-web:v1.0

# 3. Verificar el despliegue
kubectl rollout status deployment/python-app
kubectl get pods
```

### Blue-Green Deployment

Para deployments Blue-Green:

```bash
# 1. Deploy versión Green
kubectl apply -f k8s/deployment-green.yaml
kubectl set image deployment/python-app-green \
  python-app=<ECR_REPO>/python-web:v2.0

# 2. Esperar a que esté listo
kubectl rollout status deployment/python-app-green

# 3. Cambiar tráfico al Service
kubectl patch service python-app \
  -p '{"spec":{"selector":{"version":"green"}}}'

# 4. Verificar
curl http://<LOAD_BALANCER_URL>
```

## Kubernetes Manifests

### Deployment Example

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-web
  labels:
    app: python-web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-web
  template:
    metadata:
      labels:
        app: python-web
        version: v1.0
    spec:
      containers:
      - name: python-web
        image: <YOUR_REGISTRY>/python-web:latest
        ports:
        - containerPort: 5000
        env:
        - name: APP_VERSION
          value: "1.0.0"
        - name: ENVIRONMENT
          value: "production"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
```

### Service Example

```yaml
apiVersion: v1
kind: Service
metadata:
  name: python-web
spec:
  type: LoadBalancer
  selector:
    app: python-web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
```

## Seguridad

### Buenas Prácticas Implementadas

1. **Imagen Base Mínima**: Uso de `python:3.9-slim` para reducir superficie de ataque
2. **Multi-stage Build**: Separa dependencias de build de runtime
3. **No Root User**: El contenedor no corre como root (recomendado añadir)
4. **Secrets Management**: Variables sensibles mediante variables de entorno
5. **Health Checks**: Endpoints para verificar el estado de la aplicación

### Escaneo de Vulnerabilidades

```bash
# Escanear imagen Docker
docker scan python-web-iac:latest

# O con Trivy
trivy image python-web-iac:latest
```

## Testing

### Test Manual

```bash
# Health check
curl -I http://localhost:5000/health

# Verificar versión
curl http://localhost:5000/version

# Test de carga básico
ab -n 1000 -c 10 http://localhost:5000/
```

### Tests Automatizados

Puedes añadir tests con pytest:

```python
# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    
def test_version_endpoint(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert b'version' in response.data
```

##  Casos de Uso

Este proyecto es perfecto para:

-  **Aprendizaje**: Entender containerización y despliegues cloud
-  **Testing**: Probar estrategias de deployment (Blue-Green, Canary)
-  **Demos**: Demostrar pipelines CI/CD y IaC
-  **Portfolio**: Mostrar habilidades de DevOps y Cloud
-  **Prototipado**: Base rápida para aplicaciones web Python

## Integración con Otros Proyectos

Este repositorio es parte de un ecosistema DevOps completo:

### [Infra-AWS-EKS-Python](https://github.com/SergioCMDev/Infra-AWS-EKS-Python)
Infraestructura Terraform que despliega un cluster EKS en AWS específicamente diseñado para alojar esta aplicación. Incluye:
- VPC con subnets públicas y privadas
- Cluster EKS con node groups
- Application Load Balancer
- GitHub Actions runner
- CI/CD Blue-Green deployment

**Workflow Completo:**
```
1. Código en PythonWebForIAC (este repo)
   ↓
2. GitHub Actions construye imagen Docker
   ↓
3. Push a Amazon ECR
   ↓
4. Deploy a EKS (Infra-AWS-EKS-Python)
   ↓
5. Blue-Green switch automático
```

### [Wordpress-AWS-Terraform](https://github.com/SergioCMDev/Wordpress-and-phpMyAdmin-with-Terraform-and-AWS)
Otro ejemplo de IaC desplegando WordPress en AWS con VPC, EC2 y RDS.

## Mejoras Futuras

- [ ] Añadir tests unitarios con pytest
- [ ] Implementar logs estructurados (JSON)
- [ ] Añadir métricas de Prometheus
- [ ] Implementar caché con Redis
- [ ] Añadir autenticación JWT
- [ ] Crear Helm Chart para Kubernetes
- [ ] Implementar rate limiting
- [ ] Añadir OpenAPI/Swagger documentation

## Limpieza

### Detener contenedor local
```bash
docker stop python-web
docker rm python-web
```

### Eliminar imagen
```bash
docker rmi python-web-iac:latest
```

### Limpiar todo Docker
```bash
docker system prune -a
```

## Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'feat: añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Autor

**Sergio Cristauro Manzano**

- LinkedIn: [Sergio Cristauro](https://www.linkedin.com/in/sergio-cristauro/)
- Email: sergiocmdev@gmail.com

## Agradecimientos

- Flask community por el excelente framework
- Docker documentation
- Kubernetes best practices guides
- GitHub Actions team

---

**Si este proyecto te resulta útil, considera darle una estrella en GitHub**

**¿Preguntas?** Abre un issue

 **¿Listo para deployar?** Usa este proyecto con [Infra-AWS-EKS-Python](https://github.com/SergioCMDev/Infra-AWS-EKS-Python)
