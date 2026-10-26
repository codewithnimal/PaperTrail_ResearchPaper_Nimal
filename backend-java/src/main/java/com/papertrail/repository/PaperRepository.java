package com.papertrail.repository;

import com.papertrail.entity.Paper;
import com.papertrail.enums.PaperStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface PaperRepository extends JpaRepository<Paper, UUID> {

    Optional<Paper> findByFileHash(String fileHash);

    Page<Paper> findAllByOrderByCreatedAtDesc(Pageable pageable);

    List<Paper> findAllByIdIn(List<UUID> ids);

    List<Paper> findAllByStatus(PaperStatus status);
}
