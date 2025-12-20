package org.example.entidades;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Entity
@Table(name = "hospitales")
@Getter
@NoArgsConstructor
@ToString(exclude = {"departamentos", "pacientes"})
public class Hospital {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 200)
    private String nombre;

    @Column(nullable = false, length = 300)
    private String direccion;

    @Column(nullable = false, length = 20)
    private String telefono;

    @OneToMany(mappedBy = "hospital", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Departamento> departamentos = new ArrayList<>();

    @OneToMany(mappedBy = "hospital", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Paciente> pacientes = new ArrayList<>();

    // Constructor personalizado para Builder
    protected Hospital(HospitalBuilder builder) {
        this.nombre = validarString(builder.nombre, "El nombre del hospital no puede estar vacío");
        this.direccion = validarString(builder.direccion, "La dirección no puede estar vacía");
        this.telefono = validarString(builder.telefono, "El teléfono no puede estar vacío");
        this.departamentos = new ArrayList<>();
        this.pacientes = new ArrayList<>();
    }

    private String validarString(String valor, String mensaje) {
        if (valor == null || valor.trim().isEmpty()) {
            throw new IllegalArgumentException(mensaje);
        }
        return valor.trim();
    }

    // Métodos de gestión de relaciones bidireccionales
    public void agregarDepartamento(Departamento departamento) {
        if (!departamentos.contains(departamento)) {
            departamentos.add(departamento);
            departamento.setHospital(this);
        }
    }

    public void removerDepartamento(Departamento departamento) {
        departamentos.remove(departamento);
        departamento.setHospital(null);
    }

    public void agregarPaciente(Paciente paciente) {
        if (!pacientes.contains(paciente)) {
            pacientes.add(paciente);
            paciente.setHospital(this);
        }
    }

    public void removerPaciente(Paciente paciente) {
        pacientes.remove(paciente);
        paciente.setHospital(null);
    }

    // Getters que retornan colecciones inmutables
    public List<Departamento> getDepartamentos() {
        return Collections.unmodifiableList(departamentos);
    }

    public List<Paciente> getPacientes() {
        return Collections.unmodifiableList(pacientes);
    }

    // Getters package-private para sincronización interna
    List<Departamento> getInternalDepartamentos() {
        return departamentos;
    }

    List<Paciente> getInternalPacientes() {
        return pacientes;
    }

    // Builder manual
    public static HospitalBuilder builder() {
        return new HospitalBuilder();
    }

    public static class HospitalBuilder {
        private String nombre;
        private String direccion;
        private String telefono;

        public HospitalBuilder nombre(String nombre) {
            this.nombre = nombre;
            return this;
        }

        public HospitalBuilder direccion(String direccion) {
            this.direccion = direccion;
            return this;
        }

        public HospitalBuilder telefono(String telefono) {
            this.telefono = telefono;
            return this;
        }

        public Hospital build() {
            return new Hospital(this);
        }
    }
}
