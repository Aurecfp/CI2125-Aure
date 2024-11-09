#include <stdio.h>

#define MAX_POLYNOMIOS 10
#define MAX_GRADO 10

void leerPolinomio(int polinomio[], int grado);
void imprimirPolinomio(int polinomio[], int grado);
void sumarPolinomios(int resultado[], int polinomio[], int grado);
void mostrarMatrizCoeficientes(int polinomios[][MAX_GRADO + 1], int num_polinomios, int grado);

int main() {
    int num_polinomios, grado_max;
    
    // Solicitar número de polinomios y grado máximo
    printf("Ingrese el número de polinomios: ");
    scanf("%d", &num_polinomios);
    
    printf("Ingrese el grado máximo de los polinomios: ");
    scanf("%d", &grado_max);
    
    // Matriz para almacenar los coeficientes de cada polinomio
    int polinomios[MAX_POLYNOMIOS][MAX_GRADO + 1] = {0}; // Cada polinomio se inicializa con 0

    // Leer cada polinomio y asignar los coeficientes
    for (int i = 0; i < num_polinomios; i++) {
        printf("Ingrese los coeficientes del polinomio %d (omita los términos no presentes):\n", i + 1);
        leerPolinomio(polinomios[i], grado_max);
    }

    // Mostrar la matriz de coeficientes de los polinomios ingresados
    printf("Matriz de coeficientes:\n");
    mostrarMatrizCoeficientes(polinomios, num_polinomios, grado_max);

    // Array para el resultado final de la suma de los polinomios
    int resultado[MAX_GRADO + 1] = {0}; // Inicializado en 0

    // Sumar todos los polinomios
    for (int i = 0; i < num_polinomios; i++) {
        sumarPolinomios(resultado, polinomios[i], grado_max);
    }
    
    printf("La suma de los polinomios es: ");
    imprimirPolinomio(resultado, grado_max);
    
    return 0;
}

void leerPolinomio(int polinomio[], int grado) {
    int coeficiente, exponente;
    char continuar;
    do {
        printf("Ingrese el exponente del término (entre 0 y %d): ", grado);
        scanf("%d", &exponente);

        if (exponente >= 0 && exponente <= grado) {
            printf("Coeficiente de x^%d: ", exponente);
            scanf("%d", &coeficiente);
            polinomio[exponente] = coeficiente;
        } else {
            printf("Exponente fuera de rango. Intente de nuevo.\n");
        }

        printf("¿Desea ingresar otro término? (s/n): ");
        scanf(" %c", &continuar);
    } while (continuar == 's' || continuar == 'S');
}

void mostrarMatrizCoeficientes(int polinomios[][MAX_GRADO + 1], int num_polinomios, int grado) {
    for (int i = 0; i < num_polinomios; i++) {
        for (int j = 0; j <= grado; j++) {
            printf("%d ", polinomios[i][j]);
        }
        printf("\n");
    }
}

void imprimirPolinomio(int polinomio[], int grado) {
    int primero = 1; 
    for (int i = grado; i >= 0; i--) {
        if (polinomio[i] != 0) {
            if (!primero) {
                printf(" %c ", polinomio[i] > 0 ? '+' : '-');
            } else if (polinomio[i] < 0) {
                printf("-");
            }
            primero = 0;
            printf("%d", polinomio[i] > 0 ? polinomio[i] : -polinomio[i]);
            if (i > 1) printf("x^%d", i);
            else if (i == 1) printf("x");
        }
    }
    if (primero) printf("0"); 
    printf("\n");
}

void sumarPolinomios(int resultado[], int polinomio[], int grado) {
    for (int i = 0; i <= grado; i++) {
        resultado[i] += polinomio[i];
    }
}
