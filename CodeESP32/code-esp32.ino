#include <WiFi.h>
#include <esp_camera.h>

// ---  Replace with your Wi-Fi  ---
const char* ssid = "OPPO A58";
const char* password = "g5ci4ivg";

// --- HTTP server port 80 ---
WiFiServer server(80);

// --- Camera configuration ---
camera_config_t config;

void setup() {
  Serial.begin(115200);

   
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = 5;
  config.pin_d1 = 18;
  config.pin_d2 = 19;
  config.pin_d3 = 21;
  config.pin_d4 = 36;
  config.pin_d5 = 39;
  config.pin_d6 = 34;
  config.pin_d7 = 35;
  config.pin_xclk = 0;
  config.pin_pclk = 22;
  config.pin_vsync = 25;
  config.pin_href = 23;
  config.pin_sscb_sda = 26;
  config.pin_sscb_scl = 27;
  config.pin_pwdn = 32;
  config.pin_reset = -1;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA;  // QVGA if too slow
  config.jpeg_quality = 10;
  config.fb_count = 1;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Erreur d'initialisation de la caméra");
    return;
  }

  // --- Connexion to Wi-Fi ---
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnecté au Wi-Fi");

  // --- running the serveur ---
  server.begin();
  Serial.println("Serveur HTTP démarré");
  Serial.print("Prêt à streamer la caméra ! Allez à : http://");
  Serial.println(WiFi.localIP());
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Client connecté");
    String request = client.readStringUntil('\r');
    client.flush();

    // --- Endpoint /capture ---
    if (request.indexOf("GET /capture") != -1) {
      camera_fb_t * fb = esp_camera_fb_get();
      if (!fb) {
        Serial.println("Erreur de capture de la caméra");
        client.println("HTTP/1.1 500 Internal Server Error");
        client.println("Content-Type: text/plain");
        client.println("Access-Control-Allow-Origin: *"); // CORS header
        client.println();
        client.println("Erreur de capture de la caméra");
        client.flush();
        client.stop();
        return;
      }

      // --- Send the captured image ---
      Serial.println("Envoi de l'image...");
      client.println("HTTP/1.1 200 OK");
      client.println("Content-Type: image/jpeg");
      client.println("Content-Length: " + String(fb->len));
      client.println("Access-Control-Allow-Origin: *"); // CORS header
      client.println();
      client.write(fb->buf, fb->len);
      client.flush();
      Serial.println("Image envoyée !");
      esp_camera_fb_return(fb);
    }

    // --- Optional: handle OPTIONS preflight for CORS ---
    else if (request.indexOf("OPTIONS") != -1) {
      client.println("HTTP/1.1 204 No Content");
      client.println("Access-Control-Allow-Origin: *");
      client.println("Access-Control-Allow-Methods: GET, POST, OPTIONS");
      client.println("Access-Control-Allow-Headers: Content-Type");
      client.println();
      client.flush();
    }

    delay(1);
    client.stop();
    Serial.println("Client déconnecté");
  }
}
