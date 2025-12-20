package org.example.entidades;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "citas")
@Getter
@NoArgsConstructor
@ToString(exclude = {"paciente", "medico", "sala"})
public class Cita {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "paciente_id", nullable = false)
    @Setter
    private Paciente paciente;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "medico_id", nullable = false)
    @Setter
    private Medico medico;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sala_id", nullable = false)
    @Setter
    private Sala sala;

    @Column(name = "fecha_hora", nullable = false)
    private LocalDateTime fechaHora;

    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal costo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    @Setter
    private EstadoCita estado;

    @Column(length = 1000)
    @Setter
    private String observaciones;

    // Constructor personalizado para Builder
    protected Cita(CitaBuilder builder) {
        if (builder.paciente == null) {
            throw new IllegalArgumentException("El paciente no puede ser nulo");
        }
        if (builder.medico == null) {
            throw new IllegalArgumentException("El médico no puede ser nulo");
        }
        if (builder.sala == null) {
            throw new IllegalArgumentException("La sala no puede ser nula");
        }
        if (builder.fechaHora == null) {
            throw new IllegalArgumentException("La fecha/hora no puede ser nula");
        }
        if (builder.costo == null || builder.costo.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("El costo debe ser mayor que cero");
        }

        this.paciente = builder.paciente;
        this.medico = builder.medico;
        this.sala = builder.sala;
        this.fechaHora = builder.fechaHora;
        this.costo = builder.costo;
        this.estado = builder.estado != null ? builder.estado : EstadoCita.PROGRAMADA;
        this.observaciones = builder.observaciones;
    }

    // Método para serializar a CSV
    public String toCsvString() {
        String obs = observaciones != null ? observaciones.replaceAll(",", ";") : "";
        return String.format("%s,%s,%s,%s,%s,%s,%s",
                paciente.getDni(),
                medico.getDni(),
                sala.getNumero(),
                fechaHora.toString(),
                costo.toString(),
                estado.name(),
                obs
        );
    }

    // Builder manual
    public static CitaBuilder builder() {
        return new CitaBuilder();
    }

    public static class CitaBuilder {
        private Paciente paciente;
        private Medico medico;
        private Sala sala;
        private LocalDateTime fechaHora;
        private BigDecimal costo;
        private EstadoCita estado;
        private String observaciones;

        public CitaBuilder paciente(Paciente paciente) {
            this.paciente = paciente;
            return this;
        }

        public CitaBuilder medico(Medico medico) {
            this.medico = medico;
            return this;
        }

        public CitaBuilder sala(Sala sala) {
            this.sala = sala;
            return this;
        }

        public CitaBuilder fechaHora(LocalDateTime fechaHora) {
            this.fechaHora = fechaHora;
            return this;
        }

        public CitaBuilder costo(BigDecimal costo) {
            this.costo = costo;
            return this;
        }

        public CitaBuilder estado(EstadoCita estado) {
            this.estado = estado;
            return this;
        }

        public CitaBuilder observaciones(String observaciones) {
            this.observaciones = observaciones;
            return this;
        }

        public Cita build() {
            return new Cita(this);
        }
    }
}
