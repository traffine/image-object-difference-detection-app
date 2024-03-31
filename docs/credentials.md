## Instructions for creating credentials.json

## Create credentials.json

1. from the GCP console, click "IAM & Admin" > "Service Accounts".

![credentials.json | 1](/docs/images/credentials/credentials_1.png)

---

2. Click "CREATE SERVICE ACCOUNT".

![credentials.json | 2](/docs/images/credentials/credentials_2.png)

---

3. Enter any `service account name`. In the example, we enter `vision-api`.
   Click `DONE` to create the service account.

![credentials.json | 3](/docs/images/credentials/credentials_3.png)

---

4. Click on the service account you created, go to the "KEYS" tab, and click on "ADD KEY" > "Create new key".

![credentials.json | 4](/docs/images/credentials/credentials_4.png)
![credentials.json | 5](/docs/images/credentials/credentials_5.png)

---

5. Select "JSON" and click "CREATE" to download the Json file.

![credentials.json | 6](/docs/images/credentials/credentials_6.png)

---

6. Rename the downloaded Json file to `credentials.json` and add it to the root directory.

## Enable Google Vision API

To use Google Vision API, you need to activate the API by following the steps below.

1. type "google vision api" in the search field at the top of the GCP console. Click on "Cloud Vision API" when it appears.

![Google Vision API | 1](/docs/images/credentials/vision_api_1.png)

---

2. The Cloud Vision API can be activated on the destination screen.

![Google Vision API | 2](/docs/images/credentials/vision_api_2.png)
