import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data  //getter, setter, toString, equals, hashcode, etc
@Builder
@NoArgsConstructor //constructor vacio
@AllArgsConstructor // cosntructores con todos los parametros
public class Escritura {

    private int numeroEscritura;
    private Lote lote;
    private RegistroPropiedad registro;

    private String fechaEscritura;
}
