param imageTag string
param applicationInsightsId string
param solutionName string
@secure()
param appSettings object = {}
param appServicePlanId string

var imageName = 'DOCKER|kmcontainerreg.azurecr.io/km-app:${imageTag}'
var name = '${solutionName}-app'

module appService 'deploy_app_service.bicep' = {
  name: '${name}-app-module'
  params: {
    solutionName: name
    appServicePlanId: appServicePlanId
    appImageName: imageName
    appSettings: union(
      appSettings,
      {
        APPINSIGHTS_INSTRUMENTATIONKEY: reference(applicationInsightsId, '2015-05-01').InstrumentationKey
      }
    )
  }
}

output appUrl string = appService.outputs.appUrl
