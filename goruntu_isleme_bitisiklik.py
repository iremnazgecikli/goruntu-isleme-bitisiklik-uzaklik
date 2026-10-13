import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import sys

# HESAPLAMA SINIFI
class GoruntuHesaplamalari:
    @staticmethod
    def hesapla_4_bitisiklik(matrix, r, c):
        V = matrix[r][c]
        komşular = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] #(x-1,y), (x+1,y), (x,y+1), (x,y-1)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and matrix[nr][nc] == V:
                komşular.append((nr, nc))
        return komşular

    @staticmethod
    def hesapla_8_bitisiklik(matrix, r, c):
        V = matrix[r][c]
        komşular = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < 10 and 0 <= nc < 10 and matrix[nr][nc] == V:
                    komşular.append((nr, nc))
        return komşular

    @staticmethod
    def hesapla_m_bitisiklik(matrix, r, c):
        V = matrix[r][c]
        komşular = []
        # sadece köşegen kuralına göre m bitişik için
        nd = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in nd:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and matrix[nr][nc] == V:
                c1_ok = (0 <= nc < 10) and (matrix[r][nc] == V)
                c2_ok = (0 <= nr < 10) and (matrix[nr][c] == V)
                if c1_ok or c2_ok:
                    komşular.append((nr, nc))
        return komşular

    @staticmethod
    def hesapla_mesafeler(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        euclidean = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        city_block = abs(x1 - x2) + abs(y1 - y2)
        chessboard = max(abs(x1 - x2), abs(y1 - y2))
        return {
            "euclidean": euclidean,
            "city_block": city_block,
            "chessboard": chessboard
        }

#  ARAYÜZ SINIFI 
class GoruntuIslemeBitisiklikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("goruntu_isleme_bitisiklik - Görüntü İşleme Arayüzü")
        self.root.geometry("850x720")
        self.root.config(bg="#AD0E0E")

        self.matrix_size = 10
        self.matrix = [[random.randint(0, 1) for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]
        
        self.selected_p1 = None
        self.dist_p1 = None
        self.dist_p2 = None

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            pass
        
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_adjacency = ttk.Frame(self.notebook)
        self.tab_distance = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_adjacency, text=" 1. Bitişiklik Analizi ")
        self.notebook.add(self.tab_distance, text=" 2. Uzaklık Hesaplamaları ")

        self.setup_adjacency_tab()
        self.setup_distance_tab()
        self.update_all_matrices()

    def generate_new_matrix(self):
        for r in range(self.matrix_size):
            for c in range(self.matrix_size):
                self.matrix[r][c] = random.randint(0, 1)
        self.selected_p1 = None
        self.dist_p1 = None
        self.dist_p2 = None
        self.update_all_matrices()
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "Yeni 10x10 matris üretildi.\n")
        self.lbl_dist_result.config(text="Lütfen Uzaklık sekmesinden iki nokta seçin.")

    def update_all_matrices(self):
        for r in range(self.matrix_size):
            for c in range(self.matrix_size):
                val = str(self.matrix[r][c])
                self.adj_buttons[r][c].config(text=val, bg="white")
                self.dist_buttons[r][c].config(text=val, bg="white")

    def setup_adjacency_tab(self):
        top_frame = tk.Frame(self.tab_adjacency, bg="#f1f5f9", pady=10)
        top_frame.pack(fill="x")

        tk.Button(top_frame, text="Yeni Matris Üret", command=self.generate_new_matrix, bg="#cbd5e1", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(top_frame, text="4-Bitişiklik", command=self.calc_4_adj, bg="#86efac", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(top_frame, text="8-Bitişiklik", command=self.calc_8_adj, bg="#fef08a", font=("Arial", 9, "bold")).pack(side="left", padx=5)
        tk.Button(top_frame, text="m-Bitişiklik", command=self.calc_m_adj, bg="#fed7aa", font=("Arial", 9, "bold")).pack(side="left", padx=5)

        matrix_container = tk.Frame(self.tab_adjacency, bg="#475569", padx=5, pady=5)
        matrix_container.pack(pady=10)

        self.adj_buttons = [[None]*10 for _ in range(10)]
        for r in range(10):
            for c in range(10):
                b = tk.Button(matrix_container, text="0", width=4, height=2, font=("Arial", 10, "bold"),
                              command=lambda row=r, col=c: self.on_adj_click(row, col))
                b.grid(row=r, column=c, padx=2, pady=2)
                self.adj_buttons[r][c] = b

        log_frame = tk.LabelFrame(self.tab_adjacency, text=" Koordinat ve İşlem Sonuçları ", font=("Arial", 10, "bold"), padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.log_text = tk.Text(log_frame, height=6, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def on_adj_click(self, r, c):
        for i in range(10):
            for j in range(10):
                self.adj_buttons[i][j].config(bg="white")

        self.selected_p1 = (r, c)
        self.adj_buttons[r][c].config(bg="#93c5fd")
        self.log_text.insert(tk.END, f"Seçilen Piksel: ({r}, {c}) = Değer: {self.matrix[r][c]}\n")
        self.log_text.see(tk.END)

    def calc_4_adj(self):
        if not self.selected_p1:
            messagebox.showwarning("Uyarı", "Lütfen önce matristen bir piksel seçin!")
            return
        r, c = self.selected_p1
        V = self.matrix[r][c]
        self.log_text.insert(tk.END, f"\n--- 4-Bitişiklik (V={V}) ---\n")
        
        komşular = GoruntuHesaplamalari.hesapla_4_bitisiklik(self.matrix, r, c)
        for nr, nc in komşular:
            self.adj_buttons[nr][nc].config(bg="#ae1e13")
            self.log_text.insert(tk.END, f"Komşu: ({nr}, {nc})\n")

    def calc_8_adj(self):
        if not self.selected_p1:
            messagebox.showwarning("Uyarı", "Lütfen önce matristen bir piksel seçin!")
            return
        r, c = self.selected_p1
        V = self.matrix[r][c]
        self.log_text.insert(tk.END, f"\n--- 8-Bitişiklik (V={V}) ---\n")
        
        komşular = GoruntuHesaplamalari.hesapla_8_bitisiklik(self.matrix, r, c)
        for nr, nc in komşular:
            self.adj_buttons[nr][nc].config(bg="#e8979fa5")
            self.log_text.insert(tk.END, f"Komşu: ({nr}, {nc})\n")

    def calc_m_adj(self):
        if not self.selected_p1:
            messagebox.showwarning("Uyarı", "Lütfen önce matristen bir piksel seçin!")
            return
        r, c = self.selected_p1
        V = self.matrix[r][c]
        self.log_text.insert(tk.END, f"\n--- m-Bitişiklik (V={V}) ---\n")
        
        komşular = GoruntuHesaplamalari.hesapla_m_bitisiklik(self.matrix, r, c)
        for nr, nc in komşular:
            self.adj_buttons[nr][nc].config(bg="#c41b21")
            self.log_text.insert(tk.END, f"m-Komşu: ({nr}, {nc})\n")

    def setup_distance_tab(self):
        top_frame = tk.Frame(self.tab_distance, bg="#9c3d38", pady=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Mesafe için matristen sırasıyla iki hücreye tıklayın:", font=("Arial", 9, "italic"), bg="#f1f5f9").pack(side="left", padx=5)
        tk.Button(top_frame, text="Seçimleri Sıfırla", command=self.reset_distances, bg="#fca5a5", font=("Arial", 9, "bold")).pack(side="right", padx=5)

        dist_container = tk.Frame(self.tab_distance, bg="#475569", padx=5, pady=5)
        dist_container.pack(pady=10)

        self.dist_buttons = [[None]*10 for _ in range(10)]
        for r in range(10):
            for c in range(10):
                b = tk.Button(dist_container, text="0", width=4, height=2, font=("Arial", 10, "bold"),
                              command=lambda row=r, col=c: self.on_dist_click(row, col))
                b.grid(row=r, column=c, padx=2, pady=2)
                self.dist_buttons[r][c] = b

        result_frame = tk.LabelFrame(self.tab_distance, text=" Uzaklık Metrikleri Sonucu ", font=("Arial", 10, "bold"), padx=15, pady=15)
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.lbl_dist_result = tk.Label(result_frame, text="Lütfen matristen 2 nokta seçin.", font=("Arial", 11), justify="left", bg="white", padx=10, pady=10, relief="solid", bd=1)
        self.lbl_dist_result.pack(fill="both", expand=True)

    def on_dist_click(self, r, c):
        if self.dist_p1 is None or (self.dist_p1 is not None and self.dist_p2 is not None):
            self.reset_distances()
            self.dist_p1 = (r, c)
            self.dist_buttons[r][c].config(bg="#93c5fd")
            self.lbl_dist_result.config(text=f"1. Nokta Seçildi: P1({r}, {c})\nLütfen 2. Noktayı seçin...")
        else:
            self.dist_p2 = (r, c)
            self.dist_buttons[r][c].config(bg="#fca5a5")
            self.calculate_all_distances()

    def reset_distances(self):
        self.dist_p1 = None
        self.dist_p2 = None
        for r in range(10):
            for c in range(10):
                self.dist_buttons[r][c].config(bg="white")
        self.lbl_dist_result.config(text="Lütfen matristen 2 nokta seçin.")

    def calculate_all_distances(self):
        p1 = self.dist_p1
        p2 = self.dist_p2
        
        sonuclar = GoruntuHesaplamalari.hesapla_mesafeler(p1, p2)
        
        result_text = (
            f"Seçilen Noktalar:\n"
            f" • P1 = {p1} (Değer: {self.matrix[p1[0]][p1[1]]})\n"
            f" • P2 = {p2} (Değer: {self.matrix[p2[0]][p2[1]]})\n\n"
            f"----------------------------------------\n"
            f" 1. Öklid Uzaklığı (De)       : {sonuclar['euclidean']:.4f}\n"
            f" 2. City-block Uzaklığı (D4)   : {sonuclar['city_block']}\n"
            f" 3. Satranç Tahtası Uzaklığı (D8): {sonuclar['chessboard']}\n"
        )
        self.lbl_dist_result.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    
    # Mac (macOS) ekran odaklama düzeltmesi
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    app = GoruntuIslemeBitisiklikApp(root)
    root.mainloop()