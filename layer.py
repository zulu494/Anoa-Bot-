from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import AvailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import UnavailablePresenceProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import PresenceProtocolEntity
from yowsup.common.tools import Jid
from session import Session
from dataset import Dataset
import time, random, re, nlp, berita

data = Dataset().extract('')
session = Session()

class MainLayer(YowInterfaceLayer):
    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def welcomeMessage(self, namemitt, recipient):
        petunjuk = "Untuk menggunakan bot, ketik salah satu angka dibawah ini:\n\n"\
            "1. Cek SMS Penipuan\n"\
            "2. Cek Berita Hoax\n"\
            "0. Kembali ke Menu"

        self.toLower(TextMessageProtocolEntity("Halo, {} ! Bot Anti Hoax Disini 👋".format(namemitt), to=recipient))
        self.toLower(TextMessageProtocolEntity(petunjuk, to=recipient))
    
    def cariBerita(self, message):
        template = ""
        berita = berita.get_berita(message)
        berita_hits = berita['hits']

        if berita['found'] >= 1:
            ambil_berita = berita_hits[0]
            konten = ambil_berita['document']
            link_berita = konten['link']
            title = konten['title']
            template += "Hasil validasi berita dari kami:\n"
                "{}\n"
                "Link Artikel: {}\n".format(title, link_berita)
        else:
            template += "Mohon maaf, kami tidak dapat menemukan artikel yang anda cari."

        return template

    def onTextMessage(self, messageProtocolEntity):
        self.toLower(messageProtocolEntity.ack())
        time.sleep(random.randrange(2,4))
        self.toLower(AvailablePresenceProtocolEntity())
        time.sleep(random.randrange(1,2))
        self.toLower(messageProtocolEntity.ack(True))
        time.sleep(random.randrange(1,2))
        self.toLower(OutgoingChatstateProtocolEntity(
            OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(messageProtocolEntity.getFrom(False))
        ))
        time.sleep(random.randrange(1,2))
        self.toLower(OutgoingChatstateProtocolEntity(
            OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(messageProtocolEntity.getFrom(False))
        ))

        namemitt = messageProtocolEntity.getNotify()
        message = messageProtocolEntity.getBody().lower().replace('\b', '').replace('\n', '')
        recipient = messageProtocolEntity.getFrom()
        current_session = session.get(recipient)

        if current_session in [1, 2] and message == '0':
            session.set(receipt)
            self.welcomeMessage(namemitt, receipt)
        elif current_session == 0 and message in ['1', '2']:
            session.set(recipient, int(message))
            template = ""
            if int(message) == 1:
                template += "📋 Salin dan tempel pesan disini untuk pengecekan."
            else:
                template += "🔍 Masukkan kata kunci berita yang ingin divalidasi. Misalnya: *vaksin babi*."
                
            template += "\n\nKetik *0* untuk kembali ke menu."
            self.toLower(TextMessageProtocolEntity(template, to=recipient))
        else:
            if current_session == 0:
                self.welcomeMessage(namemitt, recipient)
            elif current_session == 1:
                label = nlp.get_label(message)
                self.toLower(TextMessageProtocolEntity("Hasil analisis sistem untuk pesan tersebut adalah *{}*.".format(label), to=recipient))

                time.sleep(random.randrange(2,4))
                himbauan = "❗ Kami menghimbau untuk ❗ \n\n"\
                    "- Tidak memberikan kode OTP kepada siapapun.\n"\
                    "- Selalu berhati-hati dalam memasukkan data pribadi.\n"\
                    "- Selalu cek keaslian website tersebut dengan melakukan validasi.\n"\
                    "- Jangan mudah tergiur penawaran dari SMS.\n\n"\
                    "Selalu waspada dan bijak dalam menggunakan internet. Jika ada pesan atau informasi yang mencurigakan harap lapor segera ke akun sosial media resmi terkait.\n\n"\
                    "Terima kasih."
                self.toLower(TextMessageProtocolEntity(himbauan, to=recipient))
            elif current_session == 2:
                berita = self.cariBerita(message)
                self.toLower(TextMessageProtocolEntity(berita, to=recipient))
            
        time.sleep(random.randrange(4,5))
        self.toLower(UnavailablePresenceProtocolEntity())

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onStateDisconnected(self, layerEvent):
        print("WhatsApp-Plugin : Message " + layerEvent.getArg("reason"))

        if layerEvent.getArg("reason") == 'Ping Timeout' or layerEvent.getArg("reason") == 'Connection Closed' or layerEvent.getArg("reason").find('Temporar$'):
            time.sleep(random.randint(5,15))
            print("WhatsApp-Plugin : Issueing EVENT_STATE_DISCONNECT")

            self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
            time.sleep(random.randint(5,15))
            print("WhatsApp-Plugin : Issueing EVENT_STATE_CONNECT")

            self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        elif layerEvent.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            print("WhatsApp-Plugin : Connected")