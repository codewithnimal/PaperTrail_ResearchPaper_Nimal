package com.papertrail.repository;

import com.papertrail.entity.ComparisonResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ComparisonResultRepository extends JpaRepository<ComparisonResult, UUID> {

    Optional<ComparisonResult> findByJobId(UUID jobId);
}
