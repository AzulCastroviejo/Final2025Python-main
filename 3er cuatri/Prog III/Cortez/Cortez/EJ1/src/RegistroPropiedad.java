import lombok.Builder;
import lombok.Data;

import java.util.ArrayList;
import java.util.List;

@Data
@Builder
public class RegistroPropiedad {

    private int idRegistro;
    private String nombreRegistro;
    private static int nextNumeroEscritura = 0;

    @Builder.Default
    private List<Escritura> escrituras = new ArrayList<>();

    public void registrarLote(Lote lote, String fechaEscritura){
        nextNumeroEscritura = nextNumeroEscritura + 1;
        System.out.println(nextNumeroEscritura);
        Escritura escritura = new Escritura (nextNumeroEscritura, lote, this, fechaEscritura);

        escrituras.add(escritura);
        System.out.println("Lote reguistrado en "+ nombreRegistro+ " con Escritura numero: "+nextNumeroEscritura);

    }

    public void construirEdificio(Lote lote, Edificio edificio){
        if (lote.isConstruible()) {
            lote.setEdificioConstruido(edificio);
            System.out.println("Edificio " + edificio.getNombre() + " construido en el lote "+ lote.getIdPadron());
        }else {
            System.out.println("No se puede cosntruir en el lote "+ lote.getIdPadron()+ "porque ya tiene un edificio");;
        }
    }






}
