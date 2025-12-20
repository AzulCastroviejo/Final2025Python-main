

public class Perro extends Animal {
    private String idChip;
    private Raza raza;

    @Override
    public String getIdentificacion() {
        return "Chip: " + idChip;
    }
}
