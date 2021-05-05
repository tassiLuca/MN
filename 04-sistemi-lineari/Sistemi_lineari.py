# -*- coding: utf-8 -*-
"""
04 - File per la soluzione di sistemi Lineari
"""
import numpy as np

# ------------------------------------------------------------------------------
# Metodi di sostituzione per la risoluzione di sistemi lineari con matrice 
# dei coefficienti triangolare.
# ------------------------------------------------------------------------------

def _solve_applicability(L, m, n):
    '''
    Funzione per check di applicabilità dei metodi di sostituzione in avanti e 
    all'indietro per  la risoluzione di sistemi lineari con matrice triangolare.
    
    Parametri
    ----------
    L :     Matrice triangolare inferiore.
    m, n:   Numero di righe e colonne della matrice L.

    Valori di ritorno.
    -------
    flag :  Booleano che è 0 se sono soddisfatti entrambi i test di 
            applicabilità, 1 altrimenti.
    '''
    
    # Test dimensione
    if n != m:
        print('Errore: matrice non quadrata.')
        return 1
    
    # Test singolarità: è necessario che tutti gli elementi diagonali di L
    # siano NON nulli (visto che il determinante di una matrice triangolare 
    # si calcola come il prodotto degli elementi sulla diagonale).
    # NON SI DOVREBBE FARE UN CONTROLLO CON EPS?
    if np.all(np.diag(L)) != True:
        print('Errore: Elemento diagonale nullo.') 
        return 1
     
def Lsolve(L,b): 
    """  
    Risoluzione con procedura forward di Lx=b con L triangolare inferiore.
        
    Parametri
    ----------
    L: Matrice triangolare inferiore.
    b: Termine noto.

    Valori di ritorno.
    -------
    flag :  Booleano che è 0 se sono soddisfatti i test di applicabilità.            
    x :     Soluzione del sistema lineare.
    """
    
    m, n = L.shape
    if _solve_applicability(L, m, n) :
        return [], 1
     
    # Preallocazione vettore soluzione
    x = np.zeros((n, 1))
    # N.B.: range(n) va da zero (se non specificato lo start) a n escluso.
    for i in range(n):
        # scalare = vettore riga * vettore colonna
        s = np.dot(L[i,:i], x[:i]) # sommatoria
        x[i] = (b[i] - s) / L[i,i]
    return x, 0

def Usolve(U, b):
    """  
    Risoluzione con procedura backward di Ux=b con U triangolare superiore.
        
    Parametri
    ----------
    U: Matrice triangolare superiore.
    b: Termine noto.

    Valori di ritorno.
    -------
    flag :  Booleano che è 0 se sono soddisfatti i test di applicabilità.            
    x :     Soluzione del sistema lineare.
    """
    m, n = U.shape
    if _solve_applicability(U, m, n) :
        return [], 1
     
    # Preallocazione vettore soluzione
    x = np.zeros((n, 1))
    # N.B.: range(n) va da n-1 a 0.
    for i in range(n - 1, -1, -1):
        # scalare = vettore riga * vettore colonna
        s = np.dot(U[i, i+1:n], x[i+1:n]) # sommatoria
        x[i] = (b[i] - s) / U[i,i]
    return x, 0

# ------------------------------------------------------------------------------
# Metodo di Gauss (o eliminazione gaussiana).
# ------------------------------------------------------------------------------

def LU_nopivot(A):
    """  
    Fattorizzazione PA = LU senza pivoting **versione vettorizzata**
        
    Parametri
    ----------
    A: Matrice dei coefficienti.

    Valori di ritorno.
    -------
    L: Matrice triangolare inferiore
    U: Matrice triangolare superiore
    P: Matrice identità (senza pivoting non vi è alcuna matrice di permutazione)
    """

    # Test dimensione
    m, n = A.shape
   
    flag = 0;
    if n != m:
      print("Matrice non quadrata")
      L, U, P, flag = [], [], [], 1 
      return P, L, U, flag
  
    P = np.eye(n);
    U=A.copy();
 # Fattorizzazione
    for k in range(n-1):
       #Test pivot 
          if U[k,k]==0:
            print('elemento diagonale nullo')
            L,U,P,flag=[],[],[],1 
            return P,L,U,flag

  #     Eliminazione gaussiana
          U[k+1:n,k]=U[k+1:n,k]/U[k,k]                                   # Memorizza i moltiplicatori      
          U[k+1:n,k+1:n]=U[k+1:n,k+1:n]-np.outer(U[k+1:n,k],U[k,k+1:n])  # Eliminazione gaussiana sulla matrice
     
  
    L=np.tril(U,-1)+np.eye(n)  # Estrae i moltiplicatori 
    U=np.triu(U)           # Estrae la parte triangolare superiore + diagonale
    return P,L,U,flag

def LU_nopivotv(A):
    """
    % Fattorizzazione PA=LU senza pivot   versione vettorizzata intermedia
    In output:
    L matrice triangolare inferiore
    U matrice triangolare superiore
    P matrice identità
    tali che  LU=PA=A
    """
    # Test dimensione
    m,n=A.shape
   
    flag=0;
    if n!=m:
      print("Matrice non quadrata")
      L,U,P,flag=[],[],[],1 
      return P,L,U,flag
  
    P=np.eye(n);
    U=A.copy();
 # Fattorizzazione
    for k in range(n-1):
       #Test pivot 
          if U[k,k]==0:
            print('elemento diagonale nullo')
            L,U,P,flag=[],[],[],1 
            return P,L,U,flag

  #     Eliminazione gaussiana
          for i in range(k+1,n):
             U[i,k]=U[i,k]/U[k,k]                                   # Memorizza i moltiplicatori      
             U[i,k+1:n]=U[i,k+1:n]-U[i,k]*U[k,k+1:n]  # Eliminazione gaussiana sulla matrice
     
  
    L=np.tril(U,-1)+np.eye(n)  # Estrae i moltiplicatori 
    U=np.triu(U)           # Estrae la parte triangolare superiore + diagonale
    return P,L,U,flag



def LU_nopivotb(A):
    """  
    Fattorizzazione PA = LU senza pivoting **versione base**
        
    Parametri
    ----------
    A: Matrice dei coefficienti.

    Valori di ritorno.
    -------
    L: Matrice triangolare inferiore
    U: Matrice triangolare superiore
    P: Matrice identità (senza pivoting non vi è alcuna matrice di permutazione)
    """

    # Test dimensione
    m, n = A.shape
    flag = 0;
    if n != m:
        print("Matrice non quadrata")
        L, U, P, flag = [], [], [], 1 
        return P, L, U, flag
  
    # Inizializzo la matrice di permutazione con l'identità
    P = np.eye(n)
    U = A.copy()
    # Fattorizzazione - ciclo esterno: sono necessari n - 1 passi per la fattorizzazione di U.
    for k in range(n-1):
        # Test pivot: i minori principali della matrice A devono essere diversi da zero.
        if U[k, k] == 0:
            print('elemento diagonale nullo')
            L, U, P, flag = [], [], [], 1 
            return P, L, U, flag

        '''
        Al primo passo, si annullano tutti i coefficienti della prima colonna dalla seconda riga fino all'n-esima. 
        Al secondo tutti i coefficienti della seconda colonna dalla terza riga fino all'n-esima.
        ...
        Al passo k tutti i coefficienti della k-esima colonna dalla (k+1)-esima riga fino all'n-esima.
        
        => ciclo per i = k + 1 fino a n
        
        Per far ciò devo calcolare i corrispondenti moltiplicatori, che memorizzo direttamente nella colonna k-esima
        sotto l'elemento diagonale k+1. Questo lo posso far in virtù del fatto che tutti i coefficienti del triangolo
        inferiore diventeranno nulli e che l'elemento u(i,j) del passo (k+1)-esimo è ottenuto a partire da
        u(i,j) - m(i,k) * u(k,j) del passo k-esimo.
        
                                                       Passo k = 1:    
                                                 calcolo moltiplicatori
                                                 
        | u(1,1)  u(1,2)  ...  u(1,n) |     | u(1,1)  u(1,2)  ...  u(1,n) |       
        | u(2,1)  u(2,2)  ...  u(2,n) |     | m(2,1)  u(2,2)  ...  u(2,n) |      
        |   .       .      .     .    |     |   .        .     .     .    |      
        |   .       .      .     .    | --> |   .        .     .     .    | -->  
        |   .       .      .     .    |     |   .        .     .     .    |      
        | u(n,1)  u(n,2)  ...  u(n,n) |     | m(n,1)  u(n,2)  ...  u(n,n) |     
        
                                                             Passo k = 2 ottenuto con
                                                       u(i,j) - m(i,k) * u(k,j) del passo k = 1, 
                                                            sapendo che m(i,k) = u(i,k)       
                                                        
                                            | u(1,1)          u(1,2)         ...          u(1,n)        |
                                            | m(2,1)   u(2,2)-u(2,1)*u(1,2)  ...   u(1,n)-u(2,1)*u(1,n) |  
                                            |   .               .             .             .           |   
                                        --> |   .               .             .             .           |
                                            |   .               .             .             .           | 
                                            | m(n,1)  u(n,2)-u(n,1)*u(n-1,2) ..., u(n,n)-u(n,1)*u(n-1,n)|

        Alla fine dell'algoritmo: U è matrice in cui, nel triangolo inferiore vi sono i coefficienti moltiplicativi.
        L è quindi ottenuta aggiungendo alla matrice identità la parte triangolare inferiore di U.
        U è invece ottenuta estraendo la sua parte triangolare inferiore più la diagonale.
        '''
        for i in range(k+1, n):
            # Calcolo il moltiplicatore.
            U[i,k] = U[i,k] / U[k,k] 
            for j in range(k+1,n):                                       
                U[i,j] = U[i,j] - U[i,k] * U[k,j]  # Eliminazione gaussiana sulla matrice
     
    L = np.tril(U,-1) + np.eye(n)   # Estrae i moltiplicatori
    U = np.triu(U)                  # Estrae la parte triangolare superiore + diagonale
    return P, L, U, flag