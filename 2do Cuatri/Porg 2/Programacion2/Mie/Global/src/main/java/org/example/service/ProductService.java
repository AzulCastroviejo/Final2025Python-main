package com.project.service;


import com.project.model.Product;
import com.project.repository.ProductRepository;
import java.util.Optional;


public class ProductService {
    private ProductRepository productRepository;


    public ProductService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }


    public Optional getProductById(Long id) {
        return productRepository.findById(id);
    }


    public Product createProduct(Product product) {
        return productRepository.save(product);
    }
}


