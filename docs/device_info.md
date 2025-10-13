# Device Info Configuration

Device information is now configurable through `config.json` under the `auth.device_info` section.

## Configuration Structure

Add the following section to your `config.json`:

```json
{
  "auth": {
    "device_info": {
      "build": "global",
      "OS": "Windows 10",
      "country": "USA",
      "language": "English",
      "bundle": "",
      "version": "1.1694.152.229",
      "platform": "web",
      "pushId": ""
    }
  }
}
```

## How to Extract Device Info from Chrome DevTools

1. **Open Chrome DevTools** (F12) while playing League of Kingdoms in your browser
2. Go to the **Network** tab
3. Filter by **Fetch/XHR** requests
4. Look for a request to **`setDeviceInfo`** or **`auth/connect`** (happens during authentication)
5. Click on it and check the **Payload** or **Request** tab
6. Copy the device info values from the request payload

## Supported Values

### Operating Systems
- Windows 10
- iOS 15.3.1
- Android (various versions)

### Countries
- USA
- Various country codes

### Languages
- English
- ChineseSimplified
- ChineseTraditional
- French
- German
- Italian
- Japanese
- Korean
- Portuguese
- Russian
- Spanish
- Vietnamese

### Platforms
- web
- ios
- android

## Configuration Validation

The bot will validate that:
- The `auth` section exists in config.json
- The `device_info` object is present under the `auth` section
- If either is missing, the bot will raise a clear error message and exit
