### How to Configure the App
To ensure the app works correctly, follow these steps to set up the necessary configuration:
### 1. **Create a Configuration File**
The app uses a configuration file named `config.json` for settings. Create this file in the same directory where the script resides if it doesn't already exist. The file should contain the following JSON structure:
``` json
{
  "keep_alive": 1,
  "my_email": "your_email@example.com",
  "my_password": "your_email_password",
  "my_smtp_address": "smtp.example.com",
  "mail_to": "recipient1@example.com;recipient2@example.com",
  "my_email_signature": "\n\nBest regards,\nYour App",
  "my_lat": "YOUR_LATITUDE",
  "my_long": "YOUR_LONGITUDE"
}
```
#### Explanation of Fields:
- **`keep_alive` **:
    - Set to `1` to enable the "keep alive" feature. This ensures only one instance of the app is running at any given time.
    - Set to `0` to disable this feature.

- **`my_email` **: Your email address used to send notifications (e.g., daily quotes or alerts).
- **`my_password` **: The password for the email account specified in `my_email`.
- **`my_smtp_address` **: The SMTP server address for your email provider (e.g., Gmail's SMTP is `smtp.gmail.com`).
- **`mail_to` **: A semicolon-separated list of email addresses to send messages (e.g., recipients of quotes or notifications).
- **`my_email_signature` **: Custom signature included at the end of every email.
- **`my_lat` **: Your latitude, used to determine your location (e.g., to calculate proximity to the ISS or check weather conditions).
- **`my_long` **: Your longitude, paired with `my_lat` for location-based calculations.

### 2. **Other Required Files**
In addition to the configuration file, the app requires the following files:
#### **`keep_alive.txt` **(optional):
- This file is automatically created and managed by the app if the `keep_alive` feature is enabled.
- It stores the timestamp of the last run of the app to prevent simultaneous executions.

#### **`quotes.txt` **:
- This file should contain a list of motivational quotes, one quote per line.
- The app will randomly select a quote from this file to send as part of the daily notifications.

### 3. **Email Configuration**
Ensure the email address and SMTP server are correctly configured. If you're using a service like Gmail:
- Allow "less secure apps" or enable OAuth if required by your provider (depending on their policies).
- Ensure the SMTP address and your credentials match your email provider's requirements.

### 4. **Location Data**
Provide your current latitude and longitude (`my_lat` and `my_long`) in the `config.json` file. You can find this information using:
- Google Maps: Right-click your location on the map, and copy the coordinates.

### 5. **Run the App**
After setting up the configuration and required files:
1. Ensure all files (`config.json`, `quotes.txt`, etc.) are in the same directory as the script.
2. Run the script. The app will automatically handle the configured actions, such as:
    - Sending daily motivational quotes.
    - Alerting you if the ISS is overhead, it's nighttime, and the sky is clear.

Suggestion:
To run it in the cloud, use https://www.pythonanywhere.com/ and create a task to execute it.
