package EJ2_Reflect;

import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class ReflectionExample2 {
    public static void main(String[] args) {
        try {
            // Crear una instancia de Person
            Persona person = new Persona("John");

            // Obtener la clase de la instancia
            Class<?> clazz = person.getClass();

            // Acceder y modificar el campo privado 'name'
            Field nameField = clazz.getDeclaredField("name");
            nameField.setAccessible(true);
            nameField.set(person, "Jane");

            // Invocar el método privado 'sayHello'
            Method sayHelloMethod = clazz.getDeclaredMethod("sayHello");
            sayHelloMethod.setAccessible(true);
            sayHelloMethod.invoke(person);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

