# ai.tutor.api

my_project/
├── domain/
│ ├── entities/
│ │ └── chat_message.py # Örn. ChatMessage entity
│ ├── services/
│ │ └── chat_service.py # Domain/iş mantığı
│ ├── events/
│ │ └── chat_events.py # Domain events tanımları
│ ├── ports/
│ │ ├── event_publisher_port.py # Outbound port arayüzü
│ │ └── event_consumer_port.py # Inbound port arayüzü (isteğe bağlı)
│ └── usecases/
│ └── send_chat_message.py # SendChatMessage use case
├── application/
│ ├── adapters/
│ │ ├── rabbitmq_consumer.py # Inbound adapter
│ │ ├── rabbitmq_publisher.py # Outbound adapter
│ │ └── ...
│ ├── controllers/
│ │ └── chat_controller.py # FastAPI endpoint örn. /chat
│ └── ...
├── infrastructure/
│ ├── database/
│ ├── message_queue/
│ │ └── rabbitmq_connection.py
│ └── ...
├── main.py
└── ...

PROMPT METNİ

1. Proje Amaç ve Genel Tanım
   • AI Tutor Uygulaması: ChatGPT ile gerçek zamanlı (ses veya metin) etkileşim kurulacak.
   • Mimari Yaklaşım: Clean Architecture (domain merkezli) + Event-Driven (kuyruk sistemli) hibrit tasarım.
   • Hedef: Kolay test edilebilir, teknolojiden bağımsız domain katmanı + asenkron/ölçeklenebilir iletişim.

2. Mimarinin Temel İlkeleri

   1. Clean Architecture (Domain Merkezli Tasarım)
      • Domain Katmanı:
      • İş kuralları (entities, domain services, use cases).
      • Dış dünya (framework, kütüphane, message broker) hakkında hiçbir bağımlılık içermez.
      • Ports: Domain katmanının ihtiyaç duyduğu dış etkileşimleri tarif eden arayüzler (örn. EventPublisherPort, ChatGPTClientPort, TtsServicePort vs.).
      • Adapters: Bu port’ların gerçek implementasyonlarını barındıran katman (örn. RabbitMQPublisherAdapter, OpenAIAdapter, GoogleTTSServerAdapter vb.).
      • Frameworks & Drivers: FastAPI, veritabanı sürücüleri, RabbitMQ/Kafka client’ları gibi altyapı bağımlılıkları.
   2. Event-Driven (Kuyruk) Yapı
      • Inbound Events: Kuyruk üzerinden gelen mesajlar (örn. “Kullanıcıdan yeni metin mesajı geldi”).
      • Outbound Events: Domain içinde gerçekleşen olayların (domain events) kuyruk veya bus üzerinden yayınlanması (örn. “ChatMessageReceived”, “ChatMessageAnswered”).
      • Publish/Subscribe: Uygulamanın çeşitli parçaları bu event’leri dinleyerek (consumer) veya yayınlayarak (publisher) asenkron iletişim kurar.

3. Proje Bileşenleri

   1. Domain Katmanı
      • Entities:
      • Örnek: User, ChatSession, ChatMessage gibi domain nesneleri.
      • Use Cases:
      • Örnek: SendChatMessage, HandleIncomingAudio, GenerateChatResponse, vb.
      • Domain Events:
      • Örnek: ChatMessageReceived, ChatMessageAnswered gibi olaylar, domain içinde tetiklenir.
      • Ports:
      • EventPublisherPort, ChatGPTClientPort, STTServicePort, TTSServicePort vb.
   2. Application / Adapters Katmanı
      • Inbound Adapters (Kuyruk tüketicileri, REST/WebSocket Controller’ları):
      • Örneğin: RabbitMQConsumerAdapter, ChatController (FastAPI).
      • Outbound Adapters (Kuyruk yayıncıları, dış servislere bağlanan sınıflar):
      • Örneğin: RabbitMQPublisherAdapter, OpenAIChatAdapter, GoogleTTSAdapter.
      • Mesaj Kuyruğu:
      • RabbitMQ, Kafka veya başka bir broker; rabbitmq_publisher.py, rabbitmq_consumer.py gibi dosyalar.
   3. Infrastructure Katmanı
      • Veritabanı bağlantısı, konfigürasyon, message broker setup, logging/monitoring.
      • Bu katmanla domain katmanı arasındaki iletişim, “adapter” arayüzleri üzerinden gerçekleşir.

4. ChatGPT ve Ses Entegrasyonu

   1. ChatGPT Entegrasyonu
      • Bir Outbound Port (ChatGPTClientPort) tanımlanır. Domain, sadece bu port’tan “mesaj gönder – cevap al” işlemini talep eder.
      • OpenAIAdapter bu port’u implemente ederek gerçek ChatGPT API çağrısını yapar.
      • Örneğin, ChatMessageReceived event’i tetiklenince, adapter ChatGPT’ye giden istek oluşturur ve sonrasında ChatMessageAnswered event’i yayınlar.
   2. STT/TTS Entegrasyonu (Opsiyonel)
      • Sesin metne dönüştürülmesi (STT) veya metnin sese dönüştürülmesi (TTS).
      • Bu servisler de STTServicePort, TTSServicePort gibi port’lar üzerinden entegre edilir.
      • Gelen ses sinyali -> STT -> “ChatMessageReceived” event -> ChatGPT -> cevap -> TTS -> kullanıcıya sesli yanıt.

5. Örnek Akış Senaryosu

   1. Kullanıcı mobil/web arayüzünden bir metin mesajı yollar (veya ses gönderir).
   2. Inbound Adapter (FastAPI Controller veya RabbitMQ Consumer) bu isteği alır.
   3. Domain katmanında SendChatMessage use case’i çalışır, ChatMessageReceived domain event’i oluşturulur.
   4. EventPublisherPort üzerinden bu event broker’a publish edilir.
   5. Bir Consumer (Outbound Adapter) bu event’i dinler, ChatGPT API’sine çağrı yapar ve yanıt alır.
   6. Yanıt gelince ChatMessageAnswered event’i yayınlanır.
   7. Başka bir consumer bu event’i dinleyerek kullanıcıya iletilecek cevabı TTS’e veya direkt socket’e push edebilir.

6. Prompt Kullanım Önerisi

Bu mimariyi kodla hayata geçirmek istediğimde, ChatGPT’ye şu tür bir talepte bulunacağım:

    “Yukarıdaki Clean Architecture + Event-Driven özetimize göre bir FastAPI projesi için ChatMessage entity’si, ChatGPTClientPort interface’i, RabbitMQPublisherAdapter ve OpenAIAdapter sınıflarını içeren örnek kod oluşturur musun? Aşağıdaki gibi bir dizin yapısı olsun: … (veya daha detaylı istekler).”

Böylece ChatGPT, hem mimariyi hem de tasarım kurallarını bilerek size uyumlu kod örnekleri sunabilir.

Kısacası: Bu prompt metnini saklayarak, ileride ChatGPT’ye “İşte benim planladığım mimari bu, lütfen buna uygun şekilde şu veya bu sınıfları ya da dosyaları oluştur” diye talepte bulunabilirsiniz. ChatGPT, bu sayede hangi katmanda hangi sorumlulukların olduğunu bilerek size daha tutarlı ve uyumlu kod örnekleri üretecektir.





python -m venv venv
source venv/bin/activate   # Mac/Linux

PAKETLER:
pip install fastapi "uvicorn[standard]"
