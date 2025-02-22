from web3 import Web3
import time
import getpass  # Untuk input private key secara aman

# Konfigurasi Nexus RPC
RPC_URL = "https://rpc.nexus.xyz/http"
CHAIN_ID = 392  # Nexus Chain ID

# Input Private Key secara aman
PRIVATE_KEY = getpass.getpass("Masukkan Private Key: ").strip()

# Koneksi ke Nexus RPC
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# Ambil alamat pengirim dari Private Key
try:
    sender_account = web3.eth.account.from_key(PRIVATE_KEY)
    SENDER_ADDRESS = sender_account.address
    print(f"✅  Menggunakan alamat pengirim: {SENDER_ADDRESS}")
except Exception as e:
    print("❌  Private Key tidak valid!")
    exit()

# Daftar penerima
recipients = [
    "0x04877e16bE1221D01298566d84e24C91F0859182",
    "0x031d969Ed41B98c391555a49F898a5645D325146",
    "0x087402c52dc51891e257ff2133f63259c9913be4",
    "0x0C7fa3F74b018b328144FDe3381c706342C4CBfF",
    "0x11e378C9DD7bEED43ce08e7619F78376F7dfAFbb",
    "0x1770437DC10e1cF468C3a985cAfeA74140C5A658",
    "0x1D561E1fc9535BB6a11928682A5E98a121d3C246",
    "0x2122D88cB9D51648D26176C3d7981E9eB0754801",
    "0x2e4a1b39168da8a341e08c65cf8f27589c88e32c",
    "0x2e5871c2dBe9DdC505633375FC9A3BAeb1C1F2b4",
    "0x3072FD52D9b590fd7C8d3C9E9b707fC1b4Ea0ce8",
    "0x32D0FAF8FB05FCCcd88D6E82431c3A37391C6CAC",
    "0x42Eb40652d55c25057478Fc97DdB62443d059D40",
    "0x031d969Ed41B98c391555a49F898a5645D325146",
    "0x45c6926F276513541cf093C8f08AfB187dbb6314",
    "0x53cE27073C5B9206018eD0ac5243e30a15c9CA07",
    "0x57D0AADD62ceF24550eA974e76609b75F4388A28",
    "0x593a8a6486BBD59FB71AE94D960792Dc7b4423b4",
    "0x59e467f81778eF52949976Cbe38a524034948D7A",
    "0x5BA2C092940d9f635512cEb239523a6E42B3F78f",
    "0x5a6d9a4dcb32c87d33b3c4cc88755565f24eed96",
    "0x60D99975de6d271Cef73DC607CC0Db9b79598815",
    "0x62DE6673bD37dF2808FCdc95d87a9d6E76CF80F9",
    "0x650B5c714Dad8B2aF8C495e3C35359740bcb59ab",
    "0x68e5C04e3ca65fa295eB14381a5a11CFC781F5d3",
    "0x6bf1836517DB4d58476B4De0Fe8981613C1BfbB3",
    "0x6eFb21FDa1Cac48b761ae488D3D3033F38bbE838",
    "0x7A6fD7A10d837216d20f4b0D4b9bE0F3853CDd17",
    "0x7Fb2Ae7A88a36189117A9C31962770c668BBcC75",
    "0x7d087897Ac2025130168D18Bb38eAB376661a5Ce",
    "0x81aC8f851F83fFe977DC6C1A94F19b7Ba20eB129",
    "0x840025d6c37d469856BE0b9E170b4C4623bDC9FC"
]

# Jumlah Token yang Akan Dikirim ke Setiap Penerima
AMOUNT_TO_SEND = 1  # Jumlah NEX per transaksi (dalam NEX)

# Periksa koneksi ke jaringan
if web3.is_connected():
    print("✅  Koneksi ke Nexus berhasil!")
else:
    print("❌  Gagal terhubung ke Nexus RPC!")
    exit()

# Konversi jumlah ke format yang benar (1 NEX = 10**18 Wei)
amount_in_wei = web3.to_wei(AMOUNT_TO_SEND, 'ether')

def send_token(receiver_address):
    gas_price = web3.eth.gas_price
    while True:
        try:
            nonce = web3.eth.get_transaction_count(SENDER_ADDRESS)
            tx = {
                'nonce': nonce,
                'to': receiver_address,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': gas_price,
                'chainId': CHAIN_ID
            }
            signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"✅  1 NEX terkirim ke {receiver_address}! TX Hash: {web3.to_hex(tx_hash)}")
            break
        except Exception as e:
            print(f"❌  Gagal mengirim ke {receiver_address}: {str(e)}")
            gas_price = int(gas_price * 1.2)  # Naikkan gas price 20%
            print(f"🔹 Mencoba ulang dengan gas price: {gas_price} Wei")

for recipient in recipients:
    print(f"🔹 Mengirim 1 NEX ke: {recipient}")
    send_token(recipient)
    print("⏳  Menunggu 60 detik sebelum transaksi berikutnya...")
    time.sleep(60)
