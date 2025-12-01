import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import json


class SimpleNFTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NFT Digital Rights Manager")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        self.setup_ui()
        # store minted NFTs locally for the View tab
        self.local_nfts = []
        
    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill=tk.X)
        
        title = tk.Label(
            header,
            text="NFT Digital Rights Manager", 
            font=('Arial', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=15)
        
        # Info Label
        info = tk.Label(
            self.root,
            text="Simple Testing Interface - Uses Brownie Console Commands",
            font=('Arial', 10),
            bg='#f0f0f0',
            fg='black'
        )
        info.pack(pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Mint NFT Tab
        self.mint_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.mint_tab, text='Mint NFT')
        self.setup_mint_tab()
        
        # View NFTs Tab
        self.view_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.view_tab, text='View All NFTs')
        self.setup_view_tab()
        
        # Console Output Tab
        self.console_tab = tk.Frame(self.notebook, bg='#f0f0f0')
        self.notebook.add(self.console_tab, text='Console Output')
        self.setup_console_tab()
        
    def setup_mint_tab(self):
        frame = tk.Frame(self.mint_tab, bg='#f0f0f0', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Account Index (0-9):", font=('Arial', 10), bg='#f0f0f0', fg='black').grid(row=0, column=0, sticky='w', pady=5)
        self.account_entry = tk.Entry(frame, width=10, font=('Arial', 10), fg='white', bg='#111111')
        self.account_entry.insert(0, "0")
        self.account_entry.grid(row=0, column=1, pady=5, sticky='w', padx=10)
        
        tk.Label(frame, text="Title:", font=('Arial', 10), bg='#f0f0f0', fg='black').grid(row=1, column=0, sticky='w', pady=5)
        self.title_entry = tk.Entry(frame, width=50, font=('Arial', 10), fg='white', bg='#111111')
        self.title_entry.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Description:", font=('Arial', 10), bg='#f0f0f0', fg='black').grid(row=2, column=0, sticky='nw', pady=5)
        self.desc_text = tk.Text(frame, width=38, height=4, font=('Arial', 10), fg='white', bg='#111111')
        self.desc_text.grid(row=2, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Creator Name:", font=('Arial', 10), bg='#f0f0f0', fg='black').grid(row=3, column=0, sticky='w', pady=5)
        self.creator_entry = tk.Entry(frame, width=50, font=('Arial', 10), fg='white', bg='#111111')
        self.creator_entry.grid(row=3, column=1, pady=5, padx=10)
        
        tk.Label(frame, text="Price (ETH):", font=('Arial', 10), bg='#f0f0f0', fg='black').grid(row=4, column=0, sticky='w', pady=5)
        self.price_entry = tk.Entry(frame, width=50, font=('Arial', 10), fg='white', bg='#111111')
        self.price_entry.grid(row=4, column=1, pady=5, padx=10)
        
        self.mint_button = tk.Button(
            frame,
            text="Mint NFT",
            command=self.mint_nft,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.mint_button.grid(row=5, column=0, columnspan=2, pady=20)
        
    def setup_view_tab(self):
        frame = tk.Frame(self.view_tab, bg='#f0f0f0', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        refresh_btn = tk.Button(
            frame,
            text="Refresh NFT List",
            command=self.view_nfts,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=15,
            pady=5,
            cursor='hand2'
        )
        refresh_btn.pack(pady=10)
        
        self.view_text = scrolledtext.ScrolledText(
            frame,
            width=80,
            height=20, 
            font=('Courier', 9),
            bg='#111111',
            fg='white'
        )
        self.view_text.pack(fill=tk.BOTH, expand=True)
        
    def setup_console_tab(self):
        frame = tk.Frame(self.console_tab, bg='#f0f0f0', padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            frame,
            text="Command Output:",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='black'
        ).pack(anchor='w')
        
        self.console_text = scrolledtext.ScrolledText(
            frame,
            width=80,
            height=25, 
            font=('Courier', 9),
            bg='#1e1e1e',
            fg='#00ff00'
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def run_brownie_command(self, command):
        """Run a brownie console command and return output"""
        try:
            import os

            project_root = "/Users/amarisvreshta/Downloads/BTE422/nft_project"
            scripts_dir = os.path.join(project_root, "scripts")
            os.makedirs(scripts_dir, exist_ok=True)

            script_path = os.path.join(scripts_dir, "temp_command.py")
            script = f"""
from brownie import DigitalRightsNFT, accounts

def main():
    if len(DigitalRightsNFT) == 0:
        acct = accounts[0]
        DigitalRightsNFT.deploy({{'from': acct}})

    contract = DigitalRightsNFT[-1]
    {command}
"""
            with open(script_path, "w") as f:
                f.write(script)

            result = subprocess.run(
                ["brownie", "run", script_path, "--network", "development"],
                capture_output=True,
                text=True,
                cwd=project_root,
            )

            output = result.stdout + result.stderr
            self.console_text.insert(tk.END, f"\n{'='*60}\n")
            self.console_text.insert(tk.END, f"Command: {command}\n")
            self.console_text.insert(tk.END, f"{'='*60}\n")
            self.console_text.insert(tk.END, output + "\n")
            self.console_text.see(tk.END)
            
            return result.returncode == 0, output
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.console_text.insert(tk.END, error_msg + "\n")
            self.console_text.see(tk.END)
            return False, error_msg
            
    def mint_nft(self):
        try:
            account_idx = self.account_entry.get()
            title = self.title_entry.get()
            description = self.desc_text.get("1.0", tk.END).strip()
            creator = self.creator_entry.get()
            price = self.price_entry.get()
            
            if not all([title, description, creator, price]):
                messagebox.showwarning("Warning", "Please fill all fields!")
                return
            
            price_wei = int(float(price) * 1e18)
            
            command = (
                f"tx = contract.mintNFT('{title}', '{description}', '{creator}', {price_wei}, "
                f"{{'from': accounts[{account_idx}]}})"
            )

            success, output = self.run_brownie_command(command)
            
            if success:
                messagebox.showinfo("Success", "NFT Minted Successfully!")
                self.local_nfts.append({
                    "title": title,
                    "description": description,
                    "creator": creator,
                    "price": price
                })
                # Clear fields
                self.title_entry.delete(0, tk.END)
                self.desc_text.delete("1.0", tk.END)
                self.creator_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to mint NFT. Check console output.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Minting failed:\n{str(e)}")
            
    def view_nfts(self):
        self.view_text.delete("1.0", tk.END)
        print("DEBUG: view_nfts called, local_nfts length:", len(self.local_nfts))

        if not self.local_nfts:
            self.view_text.insert(tk.END, "No NFTs minted in this session.\n")
            return

        for i, nft in enumerate(self.local_nfts):
            self.view_text.insert(tk.END, f"Token (this session) #{i}\n")
            self.view_text.insert(tk.END, f"Title: {nft['title']}\n")
            self.view_text.insert(tk.END, f"Description: {nft['description']}\n")
            self.view_text.insert(tk.END, f"Creator: {nft['creator']}\n")
            self.view_text.insert(tk.END, f"Price: {nft['price']} ETH\n")
            self.view_text.insert(tk.END, "-" * 40 + "\n")


def main():
    root = tk.Tk()
    app = SimpleNFTGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
