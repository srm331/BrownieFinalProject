import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading, os, json
from JuliaExecutor import SimpleJuliaExecutor
from brownie import NFTDRM, accounts, network

class NFTDRMApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NFT Digital Rights Manager")
        self.root.geometry("900x600")

        self.julia = SimpleJuliaExecutor()
        self.setup_gui()

    def setup_gui(self):
        ttk.Label(self.root, text="NFT DRM Platform", font=("Helvetica", 16)).pack(pady=10)
        ttk.Button(self.root, text="Mint NFT", command=self.mint_nft).pack(pady=5)
        ttk.Button(self.root, text="Buy NFT", command=self.buy_nft).pack(pady=5)
        ttk.Button(self.root, text="Owned NFTs", command=self.show_gallery).pack(pady=5)

    def mint_nft(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # Optional ML check with Julia
        result = self.julia.execute_file("julia/copyright_detector.jl")
        print(result)

        uri = f"ipfs://{os.path.basename(file_path)}"
        acct = accounts[0]
        contract = NFTDRM[-1]
        price = 1000000000000000000  # 1 ETH

        tx = contract.mintNFT(uri, price, {"from": acct})
        tx.wait(1)
        messagebox.showinfo("Minted", "NFT successfully minted!")

    def buy_nft(self):
        # Simple example for purchasing NFT ID 0
        acct = accounts[1]
        contract = NFTDRM[-1]
        tx = contract.buyNFT(0, {"from": acct, "value": contract.prices(0)})
        tx.wait(1)
        messagebox.showinfo("Purchased", "NFT purchased successfully!")

    def show_gallery(self):
        os.system("python gui/gallery_view.py")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = NFTDRMApp()
    app.run()
