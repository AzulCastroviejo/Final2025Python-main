package Reflect3;

public class DynamicInstanceExample {
    public static void main(String[] args) {
        try {
            // Obtener la clase // <?> = significa "cualquier clase"
            Class<?> clazz = Class.forName("java.util.ArrayList");
            
            // Crear una instancia de la clase
            Object instance = clazz.getDeclaredConstructor().newInstance();  //get.DeclaredCosntructor busca un cosntructor declarado

            // Comprobar el tipo de la instancia
            if (instance instanceof java.util.ArrayList) {
                System.out.println("Instancia creada exitosamente de tipo ArrayList");
            } else {
                System.out.println("La instancia no es de tipo ArrayList");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

