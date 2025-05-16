using './main.bicep'

param environmentName = readEnvironmentVariable('AZURE_ENV_NAME', 'env_name')
param contentUnderstandingLocation = readEnvironmentVariable('AZURE_CONTENT_UNDERSTANDING_LOCATION', 'swedencentral')
param secondaryLocation = readEnvironmentVariable('AZURE_SECONDARY_LOCATION', 'eastus2')
param deploymentType = readEnvironmentVariable('AZURE_OPEN_AI_MODEL_DEPLOYMENT_TYPE', 'GlobalStandard')
param gptModelName = readEnvironmentVariable('AZURE_OPEN_AI_DEPLOYMENT_MODEL', 'gpt-4o-mini')
param gptDeploymentCapacity = int(readEnvironmentVariable('AZURE_OPEN_AI_DEPLOYMENT_MODEL_CAPACITY', '30'))
param embeddingModel = readEnvironmentVariable('AZURE_OPENAI_EMBEDDING_MODEL', 'text-embedding-ada-002')
param embeddingDeploymentCapacity = int(readEnvironmentVariable('AZURE_OPENAI_EMBEDDING_MODEL_CAPACITY', '80'))
