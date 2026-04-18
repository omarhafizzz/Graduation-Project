pipeline {
    agent any

    environment {
        DOCKERHUB_USERNAME = "omarhafiz"
        IMAGE_NAME         = "${DOCKERHUB_USERNAME}/electravision"
        IMAGE_TAG          = "${BUILD_NUMBER}"
        FULL_IMAGE         = "${IMAGE_NAME}:${IMAGE_TAG}"
        SONAR_PROJECT_KEY  = "electravision"
        K8S_NAMESPACE      = "default"
        DEPLOYMENT_NAME    = "electravision"
    }

    stages {

        // ── 1. Clone ──────────────────────────────────────────────────────
        stage('Clone Repository') {
            steps {
                echo '>>> Cloning repository...'
                git branch: 'main',
                    url: 'https://github.com/omarhafizzz/graduation.git'
            }
        }

        // ── 2. SonarQube Analysis ─────────────────────────────────────────
        stage('SonarQube Analysis') {
            steps {
                echo '>>> Running SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                          -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                          -Dsonar.projectName="ElectraVision" \
                          -Dsonar.sources=. \
                          -Dsonar.language=py \
                          -Dsonar.python.version=3
                    '''
                }
            }
        }

        // // ── 3. Quality Gate ───────────────────────────────────────────────
        stage('Quality Gate') {
            steps {
                echo '>>> Waiting for SonarQube Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── 4. Build Docker Image ─────────────────────────────────────────
        stage('Build Docker Image') {
            steps {
                echo ">>> Building Docker image: ${FULL_IMAGE}"
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }

        // ── 5. Trivy Security Scan ────────────────────────────────────────
        stage('Trivy Security Scan') {
            steps {
                echo '>>> Scanning image with Trivy...'
                sh '''
                    trivy image \
                      --exit-code 0 \
                      --severity HIGH,CRITICAL \
                      --format table \
                      --output trivy-report.txt \
                      ${FULL_IMAGE}

                    echo ">>> Trivy scan complete. Report:"
                    cat trivy-report.txt
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
                }
            }
        }

        // ── 6. Push to Docker Hub ─────────────────────────────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '>>> Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin
                        docker push ${FULL_IMAGE}
                        docker tag ${FULL_IMAGE} ${IMAGE_NAME}:latest
                        docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        // ── 7. Remove Local Image ─────────────────────────────────────────
        stage('Remove Local Image') {
            steps {
                echo '>>> Removing local Docker image from EC2...'
                sh '''
                    docker rmi ${FULL_IMAGE} || true
                    docker rmi ${IMAGE_NAME}:latest || true
                    docker image prune -f || true
                '''
            }
        }

        // ── 8. Deploy to Kubernetes ───────────────────────────────────────
        stage('Deploy to Kubernetes') {
            steps {
                echo '>>> Deploying to Kubernetes...'
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        export KUBECONFIG=${KUBECONFIG}

                        # Apply manifests
                        kubectl apply -f k8s/deployment.yaml --namespace=${K8S_NAMESPACE}
                        kubectl apply -f k8s/service.yaml    --namespace=${K8S_NAMESPACE}

                        # Update image to the new build
                        kubectl set image deployment/${DEPLOYMENT_NAME} \
                            ${DEPLOYMENT_NAME}=${FULL_IMAGE} \
                            --namespace=${K8S_NAMESPACE}

                        # Wait for rollout to finish
                        kubectl rollout status deployment/${DEPLOYMENT_NAME} \
                            --namespace=${K8S_NAMESPACE} \
                            --timeout=120s

                        echo ">>> Deployment complete!"
                        kubectl get pods --namespace=${K8S_NAMESPACE}
                    '''
                }
            }
        }
    }

    // ── Post Actions ──────────────────────────────────────────────────────
    post {
        success {
            echo """
            ============================================
             Pipeline SUCCESS
             Image  : ${FULL_IMAGE}
             Build  : #${BUILD_NUMBER}
            ============================================
            """
        }
        failure {
            echo """
            ============================================
             Pipeline FAILED at stage: ${env.STAGE_NAME}
             Check the logs above for details.
            ============================================
            """
            sh 'docker image prune -f || true'
        }
        always {
            cleanWs()
        }
    }
}