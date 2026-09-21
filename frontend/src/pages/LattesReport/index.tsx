import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { getLattesReportStatus, triggerLattesReport } from "../../utils/api";
import {
  Page,
  PageContent,
  Hero,
  HeroTitle,
  HeroSubtitle,
  Panel,
  FieldLabel,
  IdsTextArea,
  FieldHint,
  SubmitButton,
  StateMessage,
  ErrorState,
  SuccessState,
  LogBox,
} from "./style";

const AnyTextArea: any = IdsTextArea;
const AnySubmitButton: any = SubmitButton;

const POLL_INTERVAL_MS = 3000;

type ReportStatus = {
  status: "never_run" | "pending" | "running" | "done" | "failed";
  extra_ids?: string[];
  ignored_duplicate_ids?: string[];
  log?: string;
  error?: string;
  report_url?: string | null;
};

const LattesReport = () => {
  const [idsInput, setIdsInput] = useState("");
  const [submitError, setSubmitError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reportStatus, setReportStatus] = useState<ReportStatus | null>(null);
  const pollTimer = useRef<ReturnType<typeof setInterval> | null>(null);

  const isRunning = reportStatus?.status === "running" || reportStatus?.status === "pending";

  const stopPolling = () => {
    if (pollTimer.current) {
      clearInterval(pollTimer.current);
      pollTimer.current = null;
    }
  };

  const fetchStatus = async () => {
    try {
      const data = await getLattesReportStatus();
      setReportStatus(data);
      if (data.status !== "running" && data.status !== "pending") {
        stopPolling();
      }
    } catch (error) {
      console.error("Erro ao consultar status do relatório Lattes:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
    return () => stopPolling();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError("");

    const extraIds = idsInput
      .split(/[\n,]/)
      .map((id) => id.trim())
      .filter(Boolean);

    setIsSubmitting(true);
    try {
      const data = await triggerLattesReport(extraIds);
      setReportStatus({ status: data.status, extra_ids: data.extra_ids });
      stopPolling();
      pollTimer.current = setInterval(fetchStatus, POLL_INTERVAL_MS);
    } catch (error: any) {
      const detail = error?.response?.data?.detail;
      setSubmitError(detail || "Erro ao iniciar a execução do scriptLattes. Tente novamente.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Page initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
      <PageContent>
        <Hero>
          <motion.div
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.4 }}
          >
            <HeroTitle>Relatório scriptLattes</HeroTitle>
            <HeroSubtitle>
              Informe IDs Lattes adicionais para incluí-los, junto com os membros de
              Farmanguinhos já processados, na próxima execução do scriptLattes.
            </HeroSubtitle>
          </motion.div>
        </Hero>

        <Panel onSubmit={handleSubmit}>
          <FieldLabel htmlFor="extra-lattes-ids">IDs Lattes adicionais</FieldLabel>
          <AnyTextArea
            id="extra-lattes-ids"
            rows={4}
            placeholder={"Um ID por linha ou separado por vírgula. Ex.: 1234567890123456"}
            value={idsInput}
            onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setIdsInput(e.target.value)}
          />
          <FieldHint>
            Cada ID Lattes deve ter 16 dígitos numéricos. IDs já processados hoje são ignorados
            automaticamente.
          </FieldHint>
          <AnySubmitButton htmlType="submit" type="primary" loading={isSubmitting || isRunning}>
            {isRunning ? "Executando..." : "Executar scriptLattes"}
          </AnySubmitButton>
        </Panel>

        {submitError && <ErrorState>{submitError}</ErrorState>}

        {!submitError && reportStatus?.status === "never_run" && (
          <StateMessage>O scriptLattes ainda não foi executado por esta página.</StateMessage>
        )}

        {isRunning && (
          <StateMessage>
            Execução em andamento. Isso pode levar alguns minutos, dependendo da quantidade de
            currículos a processar.
          </StateMessage>
        )}

        {reportStatus?.status === "failed" && (
          <ErrorState>
            Falha ao executar o scriptLattes.
            {reportStatus.error ? `\n\n${reportStatus.error}` : ""}
          </ErrorState>
        )}

        {reportStatus?.status === "done" && (
          <SuccessState>
            <strong>Relatório gerado com sucesso.</strong>
            {reportStatus.report_url && (
              <a href={reportStatus.report_url} target="_blank" rel="noreferrer">
                Abrir relatório scriptLattes
              </a>
            )}
            {reportStatus.ignored_duplicate_ids && reportStatus.ignored_duplicate_ids.length > 0 && (
              <span>
                IDs ignorados por já estarem entre os membros de Farmanguinhos:{" "}
                {reportStatus.ignored_duplicate_ids.join(", ")}
              </span>
            )}
          </SuccessState>
        )}

        {reportStatus?.log && <LogBox>{reportStatus.log}</LogBox>}
      </PageContent>
    </Page>
  );
};

export default LattesReport;
