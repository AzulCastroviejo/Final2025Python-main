package org.example;

import org.example.model.Product;
import org.example.repository.ProductRepository;
import org.example.service.ProductService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.example.Mockito.*;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

class ProductServiceTest {

    private ProductRepository mockRepo;
    private ProductService service;

    @BeforeEach
    void setUp() {
        mockRepo = mock(ProductRepository.class);
        service = new ProductService(mockRepo);
    }

    @Test
    void testFindProductByIdExists() {
        Product expected = new Product(1L, "Laptop", 1200.0);
        when(mockRepo.findById(1L)).thenReturn(Optional.of(expected));

        Product result = service.findProductById(1L);
        assertEquals("Laptop", result.getName());
        verify(mockRepo).findById(1L);
    }

    @Test
    void testFindProductByIdNotFound() {
        when(mockRepo.findById(99L)).thenReturn(Optional.empty());

        assertThrows(IllegalArgumentException.class, () -> service.findProductById(99L));
        verify(mockRepo).findById(99L);
    }
}

