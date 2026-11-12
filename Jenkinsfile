// =====================================================================
//  PIPELINE LOCAL - PetManagement
//  Checkout -> Build -> Test -> SonarQube -> Quality Gate
//  -> Docker Build -> Deploy (docker compose, máy local) -> Health Check
// =====================================================================
pipeline {
    agent any

    environment {
        APP_IMAGE         = 'petmanagement_webapp'
        IMAGE_TAG         = "${env.BUILD_NUMBER}"
        SONAR_PROJECT_KEY = 'PetManagement'
        // Jenkins chạy trong mạng docker "petnet" nên gọi app bằng tên container
        APP_HEALTH_URL    = 'http://petmanagement_webapp/health'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('1. Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --pretty=format:"Commit: %h - %s (%an)"'
            }
        }

        stage('2. Restore & Build') {
            steps {
                sh '''
                    dotnet --info | head -n 5
                    dotnet restore PetManagement.csproj
                    dotnet build PetManagement.csproj -c Release --no-restore
                '''
            }
        }

        stage('3. Unit Test') {
            steps {
                sh '''
                    dotnet test tests/PetManagement.Tests/PetManagement.Tests.csproj \
                        -c Release \
                        /p:CollectCoverage=true \
                        /p:CoverletOutputFormat=opencover
                '''
            }
        }

        stage('4. SonarQube Analysis') {
            steps {
                // 'SonarQube' = tên server cấu hình trong Manage Jenkins -> System
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        dotnet sonarscanner begin \
                            /k:"${SONAR_PROJECT_KEY}" \
                            /n:"Pet Management System" \
                            /v:"${BUILD_NUMBER}" \
                            /d:sonar.host.url="${SONAR_HOST_URL}" \
                            /d:sonar.token="${SONAR_AUTH_TOKEN}" \
                            /d:sonar.cs.opencover.reportsPaths="tests/PetManagement.Tests/coverage.opencover.xml" \
                            /d:sonar.exclusions="**/bin/**,**/obj/**,**/wwwroot/**,**/tests/**"
                        dotnet build PetManagement.csproj -c Release --no-restore
                        dotnet sonarscanner end /d:sonar.token="${SONAR_AUTH_TOKEN}"
                    '''
                }
            }
        }

        stage('5. Quality Gate') {
            steps {
                // Cần webhook SonarQube -> http://petmanagement_jenkins:8080/sonarqube-webhook/
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('6. Docker Build') {
            steps {
                sh '''
                    docker build -t ${APP_IMAGE}:${IMAGE_TAG} -t ${APP_IMAGE}:latest .
                    docker images ${APP_IMAGE}
                '''
            }
        }

        stage('7. Deploy (Local - docker compose)') {
            steps {
                sh '''
                    docker compose -f docker-compose.yml up -d --no-build
                    docker compose -f docker-compose.yml ps
                '''
            }
        }

        stage('8. Health Check') {
            steps {
                sh '''
                    for i in $(seq 1 20); do
                        if curl -fsS ${APP_HEALTH_URL}; then
                            echo ""; echo "Ứng dụng HOẠT ĐỘNG (lần thử $i)"; exit 0
                        fi
                        echo "Chờ ứng dụng khởi động... ($i/20)"; sleep 6
                    done
                    docker compose -f docker-compose.yml logs --tail=100 web
                    exit 1
                '''
            }
        }
    }

    post {
        success { echo 'PIPELINE LOCAL THÀNH CÔNG - App: http://localhost:5000' }
        failure { echo 'PIPELINE LOCAL THẤT BẠI - xem log ở trên.' }
        always  { sh 'docker image prune -f || true' }
    }
}
