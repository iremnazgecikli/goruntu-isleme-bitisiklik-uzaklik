import math

class GoruntuHesaplamalari:
    @staticmethod
    def hesapla_4_bitisiklik(matrix, r, c):
        V = matrix[r][c]
        komşular = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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
        
        # N4 komşuları
        n4 = [(-1, 0), (1, 0), (0, -1), (0, 1)] #(x-1,y), (x+1,y), (x,y+1), (x,y-1)
        for dr, dc in n4:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and matrix[nr][nc] == V:
                komşular.append((nr, nc))

        # Köşegen yani ND komşuları m-bitişiklik kuralına göre
        nd = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in nd:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10 and matrix[nr][nc] == V:
                # Ortak N4 komşularının kesişiminde V var mı kontrolü
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