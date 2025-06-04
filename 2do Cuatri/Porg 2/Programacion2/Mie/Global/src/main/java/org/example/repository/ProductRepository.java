package com.project.repository;


import com.project.model.Product;
import java.util.Optional;


public interface ProductRepository {
    Optional findById(Long id);
    Product save(Product product);
}

