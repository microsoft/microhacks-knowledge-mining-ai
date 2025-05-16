## Add Authentication in Azure App Service configuration
1. Click on `Authentication` from left menu.

  ![Authentication](../support-docs/Images/AppAuthentication.png)

2. Click on `+ Add Provider` to see a list of identity providers.

  ![Authentication Identity](../support-docs/Images/AppAuthenticationIdentity.png)

3. Click on `+ Add Provider` to see a list of identity providers.

  ![Add Provider](../support-docs/Images/AppAuthIdentityProvider.png)

4. Select the first option `Microsoft Entra Id` from the drop-down list.
 
 ![Add Provider](../support-docs/Images/AppAuthIdentityProviderAdd.png)

5. Accept the default values and click on `Add` button to go back to the previous page with the identity provider added.

 ![Add Provider](../support-docs/Images/AppAuthIdentityProviderAdded.png)

 ### Creating a new App Registration
1. Click on `Home` and select `Microsoft Entra ID`.

![Microsoft Entra ID](../support-docs/Images/MicrosoftEntraID.png)

2. Click on `App registrations`.

![App registrations](../support-docs/Images/Appregistrations.png)

3. Click on `+ New registration`.

![New Registrations](../support-docs/Images/NewRegistration.png)

4. Provide the `Name`, select supported account types as `Accounts in this organizational directory only(Contoso only - Single tenant)`, select platform as `Web`, enter/select the `URL` and register.

![Add Details](../support-docs/Images/AddDetails.png)

5. After application is created sucessfully, then click on `Add a Redirect URL`.

![Redirect URL](../support-docs/Images/AddRedirectURL.png)

6. Click on `+ Add a platform`.

![+ Add platform](../support-docs/Images/AddPlatform.png)

7. Click on `Web`.

![Web](../support-docs/Images/Web.png)

8. Enter the `web app URL` (Provide the app service name in place of XXXX) and Save. Then go back to [Step 4] and follow from _Point 4_ choose `Pick an existing app registration in this directory` from the Add an Identity Provider page and provide the newly registered App Name.

![Add Details](../support-docs/Images/WebAppURL.png)
