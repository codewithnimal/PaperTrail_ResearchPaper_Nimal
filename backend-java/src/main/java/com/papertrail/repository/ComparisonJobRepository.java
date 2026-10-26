package com.papertrail.repository;

import com.papertrail.entity.ComparisonJob;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ComparisonJobRepository extends JpaRepository<ComparisonJob, UUID> {
}
