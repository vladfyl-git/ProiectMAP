#  Simulator de Trafic Rutier (Python)

Acest proiect reprezintă implementarea **Temei 16**, un simulator de trafic rutier bazat pe evenimente discrete. Aplicația modelează fluxul de vehicule la semafoare, calculează congestia și timpii de așteptare și oferă algoritmi pentru optimizarea ciclurilor de semaforizare.

##  Descriere Proiect

Scopul simulatorului este de a modela un sistem de transport și de a analiza performanța acestuia folosind teoria cozilor.

**Ce am învățat și implementat:**
* Simulări discrete cu evenimente.
* Generarea de trafic folosind distribuții probabilistice.
* Algoritmi de optimizare pentru temporizarea semafoarelor.
* Vizualizare în timp real în consolă (text-based animation).
* Analiza comparativă a performanței (ex: 1 vs 2 vs 3 benzi).

## Funcționalități Principale

*  **Generare Trafic:** Rată configurabilă de vehicule/minut.
*  **Control Semafor:** Cicluri ajustabile (Roșu/Verde/Galben).
*  **Multi-Lane:** Suport pentru multiple benzi de circulație.
*  **Statistici:** Calcul congestie medie/maximă și timp mediu de așteptare.
*  **Optimizare Automată:** Găsirea timpului ideal pentru culoarea verde.
*  **Vizualizare:** Interfață text dinamică în timpul rulării.

---

## 📸 Exemple de Rulare și Rezultate

Mai jos sunt prezentate capturi de ecran din timpul rulării simulatorului, demonstrând diverse scenarii.

### 1. Vizualizare în Timp Real
Simularea afișează starea curentă a benzilor și culoarea semaforului.

| Stare Galben (1 Bandă) | Stare Verde (2 Benzi) |
|:---:|:---:|
| ![Galben](ss1.png) | ![Verde 2 Benzi](ss3.png) |
| *Momentul t=197s, semafor pe Galben* | *Momentul t=255s, trafic fluidizat pe 2 benzi* |

### 2. Rapoarte de Performanță
La finalul simulării, se generează un raport detaliat cu metrici de eficiență.

**Raport Standard (100 mașini):**
![Raport 100](ss2.png)

**Simulare de Volum Mare (500 mașini):**
![Raport 500](ss4.png)
*Se observă creșterea timpului de așteptare la volume mari.*

### 3. Funcții Avansate

**Optimizare Automată:**
Simulatorul poate rula scenarii multiple pentru a găsi configurația ideală.
![Optimizare](ss5.png)
*Sistemul a recomandat un timp de verde de 25s.*

**Comparație Benzi de Circulație:**
Analiza impactului adăugării de noi benzi asupra congestiei.
![Comparatie](ss6.png)
*Trecerea de la 1 la 2 benzi reduce semnificativ congestia.*

---

## 🚀 Cum se rulează (Comenzi)

Pentru a rula proiectul, asigurați-vă că aveți Python 3 instalat. Fișierul principal este `simulator.py`.

### Rulare simplă cu vizualizare
```bash
python simulator.py --cars 100 --light_cycle 30 --lanes 1 --viz
