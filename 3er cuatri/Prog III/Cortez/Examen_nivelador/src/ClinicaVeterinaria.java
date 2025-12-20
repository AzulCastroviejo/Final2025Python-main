
public class ClinicaVeterinaria {

    private ContenedorGenerico<Veterinario> staff;
    private ContenedorGenerico<Animal> pacientes;

    public ClinicaVeterinaria() {
        this.staff = new ContenedorGenerico<>();
        this.pacientes = new ContenedorGenerico<>();
    }

    public void agregarVeterinario(Veterinario v) {
        staff.agregar(v);
        System.out.println("Veterinario agregado: " + v.getNombre());
    }

    public void registrarPaciente(Animal a) {
        pacientes.agregar(a);
        System.out.println("Paciente registrado: " + a.getNombre());
    }

    // Métodos para ver listas
    public void mostrarStaff() {
        staff.getElementos().forEach(v -> System.out.println(v.getNombre()));
    }

    public void mostrarPacientes() {
        pacientes.getElementos().forEach(a -> System.out.println(a.getNombre()));
    }
}

