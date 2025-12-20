

import java.time.LocalDate;

public abstract class Animal {
    protected String nombre;
    protected int edad;
    protected LocalDate fechaNacimiento;
    protected EstadoAnimal estado;
    protected Dueno dueno;
    protected FichaMedica fichaMedica;

    public abstract String getIdentificacion();

    public String getDetalle() {
        return nombre + " (" + edad + " años)";
    }

    public boolean necesitaVacunaAnual() {
        return true; // simplificación
    }

    public String getNombre() {
        return nombre;
    }
}
