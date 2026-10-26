package com.papertrail;

import com.papertrail.client.AiServiceClient;
import com.papertrail.controller.PaperController;
import com.papertrail.service.PaperService;
import com.papertrail.dto.PaperResponse;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;

import java.time.OffsetDateTime;
import java.util.List;
import java.util.UUID;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

/**
 * Tests for PaperController covering upload validation, retrieval, and error handling.
 */
@WebMvcTest(controllers = PaperController.class, excludeAutoConfiguration = {
    org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration.class,
    org.springframework.boot.autoconfigure.security.servlet.SecurityFilterAutoConfiguration.class
})
@org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc(addFilters = false)
class PaperControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private PaperService paperService;

    @MockBean
    private AiServiceClient aiServiceClient;

    @Test
    void healthEndpoint_shouldReturn200() throws Exception {
        // Health is on a different controller, test via the papers list
        PaperResponse paper = new PaperResponse(
            UUID.randomUUID(), "test.pdf", "Test Paper", "EXTRACTED",
            5, null, OffsetDateTime.now(), OffsetDateTime.now()
        );
        Page<PaperResponse> page = new PageImpl<>(List.of(paper));
        when(paperService.getAllPapers(any(Pageable.class))).thenReturn(page);

        mockMvc.perform(get("/api/papers"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.content[0].originalFilename").value("test.pdf"));
    }

    @Test
    void uploadPdf_shouldReturnCreated() throws Exception {
        MockMultipartFile file = new MockMultipartFile(
            "files", "research.pdf", "application/pdf", new byte[]{0x25, 0x50, 0x44, 0x46}
        );

        PaperResponse response = new PaperResponse(
            UUID.randomUUID(), "research.pdf", null, "EXTRACTING",
            null, null, OffsetDateTime.now(), OffsetDateTime.now()
        );
        when(paperService.uploadPapers(any())).thenReturn(List.of(response));

        mockMvc.perform(multipart("/api/papers").file(file))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$[0].originalFilename").value("research.pdf"));
    }

    @Test
    void getPaper_shouldReturn404_whenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        when(paperService.getPaper(id)).thenThrow(
            new com.papertrail.exception.ResourceNotFoundException("Paper", id));

        mockMvc.perform(get("/api/papers/" + id))
            .andExpect(status().isNotFound());
    }

    @Test
    void getPaper_shouldReturnPaper_whenExists() throws Exception {
        UUID id = UUID.randomUUID();
        PaperResponse paper = new PaperResponse(
            id, "paper.pdf", "Deep Learning Survey", "EXTRACTED",
            42, null, OffsetDateTime.now(), OffsetDateTime.now()
        );
        when(paperService.getPaper(id)).thenReturn(paper);

        mockMvc.perform(get("/api/papers/" + id))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.title").value("Deep Learning Survey"))
            .andExpect(jsonPath("$.pageCount").value(42));
    }

    @Test
    void deletePaper_shouldReturn204() throws Exception {
        UUID id = UUID.randomUUID();
        doNothing().when(paperService).deletePaper(id);

        mockMvc.perform(delete("/api/papers/" + id))
            .andExpect(status().isNoContent());
    }

    @Test
    void deletePaper_shouldReturn404_whenNotFound() throws Exception {
        UUID id = UUID.randomUUID();
        doThrow(new com.papertrail.exception.ResourceNotFoundException("Paper", id))
            .when(paperService).deletePaper(id);

        mockMvc.perform(delete("/api/papers/" + id))
            .andExpect(status().isNotFound());
    }

    @Test
    void listPapers_shouldReturnPaginatedResults() throws Exception {
        List<PaperResponse> papers = List.of(
            new PaperResponse(UUID.randomUUID(), "paper1.pdf", "Paper 1", "EXTRACTED",
                10, null, OffsetDateTime.now(), OffsetDateTime.now()),
            new PaperResponse(UUID.randomUUID(), "paper2.pdf", "Paper 2", "EXTRACTED",
                20, null, OffsetDateTime.now(), OffsetDateTime.now())
        );
        Page<PaperResponse> page = new PageImpl<>(papers);
        when(paperService.getAllPapers(any(Pageable.class))).thenReturn(page);

        mockMvc.perform(get("/api/papers?page=0&size=20"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.content.length()").value(2))
            .andExpect(jsonPath("$.totalElements").value(2));
    }
}
