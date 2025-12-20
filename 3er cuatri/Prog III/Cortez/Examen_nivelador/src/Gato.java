

public class Gato extends Animal {
    private String color;
    private String razaFelina;

    @Override
    public String getIdentificacion() {
        return "Gato " + color + " de raza " + razaFelina;
    }
}
