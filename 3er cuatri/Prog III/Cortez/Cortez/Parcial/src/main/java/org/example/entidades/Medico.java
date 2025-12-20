package org.example.entidades;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;
import lombok.experimental.SuperBuilder;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Entity
@Table(name = "medicos")
@Getter
@SuperBuilder
@NoArgsConstructor
@ToString(callSuper = true, exclude = {"departamento", "citas"})
public class Medico extends Persona {

    @Embedded
    @Column(nullable = false, unique = true)
    private Matricula numeroMatricula;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private EspecialidadMedica especialidad;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "departamento_id")
    @Setter
    private Departamento departamento;

    @OneToMany(mappedBy = "medico", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Cita> citas = new ArrayList<>();

    // Constructor personalizado para SuperBuilder
    protected Medico(MedicoBuilder<?, ?> builder) {
        super(builder);

        if (builder.numeroMatricula == null) {
            throw new IllegalArgumentException("La matrícula no puede ser nula");
        }
        this.numeroMatricula = new Matricula(builder.numeroMatricula);

        if (builder.especialidad == null) {
            throw new IllegalArgumentException("La especialidad no puede ser nula");
        }
        this.especialidad = builder.especialidad;

        // Inicialización explícita de colecciones
        this.citas = new ArrayList<>();
    }

    // Métodos de gestión de relaciones bidireccionales
    public void addCita(Cita cita) {
        if (!citas.contains(cita)) {
            citas.add(cita);
            cita.setMedico(this);
        }
    }

    public void removeCita(Cita cita) {
        citas.remove(cita);
        cita.setMedico(null);
    }

    // Getters que retornan colecciones inmutables
    public List<Cita> getCitas() {
        return Collections.unmodifiableList(citas);
    }

    // Getter package-private para sincronización interna
    List<Cita> getInternalCitas() {
        return citas;
    }

    // Clase Builder abstracta necesaria para @SuperBuilder
    public static abstract class MedicoBuilder<C extends Medico, B extends MedicoBuilder<C, B>>
            extends PersonaBuilder<C, B> {
        // Atributo adicional para el builder
        private String numeroMatricula;

        public B numeroMatricula(String numeroMatricula) {
            this.numeroMatricula = numeroMatricula;
            return self();
        }
    }
}
