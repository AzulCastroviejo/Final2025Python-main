package org.example.entidades;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Entity
@Table(name = "salas")
@Getter
@NoArgsConstructor
@ToString(exclude = {"departamento", "citas"})
public class Sala {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 20)
    private String numero;

    @Column(nullable = false, length = 100)
    private String tipo;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "departamento_id", nullable = false)
    @Setter
    private Departamento departamento;

    @OneToMany(mappedBy = "sala", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Cita> citas = new ArrayList<>();

    // Constructor personalizado para Builder
    protected Sala(SalaBuilder builder) {
        if (builder.numero == null || builder.numero.trim().isEmpty()) {
            throw new IllegalArgumentException("El número de sala no puede estar vacío");
        }
        if (builder.tipo == null || builder.tipo.trim().isEmpty()) {
            throw new IllegalArgumentException("El tipo de sala no puede estar vacío");
        }
        if (builder.departamento == null) {
            throw new IllegalArgumentException("El departamento no puede ser nulo");
        }

        this.numero = builder.numero.trim();
        this.tipo = builder.tipo.trim();
        this.departamento = builder.departamento;
        this.citas = new ArrayList<>();
    }

    // Métodos de gestión de relaciones bidireccionales
    public void addCita(Cita cita) {
        if (!citas.contains(cita)) {
            citas.add(cita);
            cita.setSala(this);
        }
    }

    public void removeCita(Cita cita) {
        citas.remove(cita);
        cita.setSala(null);
    }

    // Getters que retornan colecciones inmutables
    public List<Cita> getCitas() {
        return Collections.unmodifiableList(citas);
    }

    // Getter package-private para sincronización interna
    List<Cita> getInternalCitas() {
        return citas;
    }

    // Builder manual
    public static SalaBuilder builder() {
        return new SalaBuilder();
    }

    public static class SalaBuilder {
        private String numero;
        private String tipo;
        private Departamento departamento;

        public SalaBuilder numero(String numero) {
            this.numero = numero;
            return this;
        }

        public SalaBuilder tipo(String tipo) {
            this.tipo = tipo;
            return this;
        }

        public SalaBuilder departamento(Departamento departamento) {
            this.departamento = departamento;
            return this;
        }

        public Sala build() {
            return new Sala(this);
        }
    }
}
