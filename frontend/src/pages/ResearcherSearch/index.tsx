import { useState } from "react";
import { motion } from "framer-motion";
import { searchResearchers } from "../../utils/api";
import ResearcherCard, { Researcher } from "../../components/ResearcherCard";
import {
  Page,
  PageContent,
  Hero,
  HeroTitle,
  HeroSubtitle,
  SearchPanel,
  SearchInput,
  SearchButton,
  ResultsHeader,
  ResultsTitle,
  ResultsCount,
  StateMessage,
  EmptyState,
  ErrorState,
} from "./style";

const AnySearchInput: any = SearchInput;
const AnySearchButton: any = SearchButton;

const ResearcherSearch = () => {
  const [searchInput, setSearchInput] = useState("");
  const [researchers, setResearchers] = useState<Researcher[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage("");
    try {
      const data = await searchResearchers(searchInput.trim());
      setResearchers(data.results || []);
      setHasSearched(true);
    } catch (error) {
      console.error("Erro ao buscar pesquisadores:", error);
      setErrorMessage("Erro ao buscar pesquisadores. Tente novamente.");
    } finally {
      setIsLoading(false);
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
            <HeroTitle>Buscar pesquisadores</HeroTitle>
            <HeroSubtitle>
              Pesquise autores cadastrados na Plataforma Lattes por tema, palavra-chave ou área
              de interesse.
            </HeroSubtitle>
          </motion.div>
        </Hero>

        <SearchPanel onSubmit={handleSubmit}>
          <AnySearchInput
            placeholder="Digite um tema, palavra-chave ou área de interesse..."
            value={searchInput}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearchInput(e.target.value)}
            allowClear
          />
          <AnySearchButton htmlType="submit" type="primary" loading={isLoading}>
            Buscar
          </AnySearchButton>
        </SearchPanel>

        {errorMessage && <ErrorState>{errorMessage}</ErrorState>}

        {hasSearched && !errorMessage && (
          <>
            <ResultsHeader>
              <ResultsTitle>Resultados da busca</ResultsTitle>
              <ResultsCount>
                {researchers.length} pesquisador(es) encontrado(s)
              </ResultsCount>
            </ResultsHeader>

            {isLoading && <StateMessage>Buscando pesquisadores...</StateMessage>}

            {!isLoading && researchers.length > 0 && (
              <motion.div
                initial="hidden"
                animate="visible"
                variants={{
                  hidden: { opacity: 0, y: 50 },
                  visible: {
                    opacity: 1,
                    y: 0,
                    transition: { staggerChildren: 0.08 },
                  },
                }}
              >
                {researchers.map((researcher) => (
                  <motion.div
                    key={researcher.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.25 }}
                  >
                    <ResearcherCard researcher={researcher} />
                  </motion.div>
                ))}
              </motion.div>
            )}

            {!isLoading && researchers.length === 0 && (
              <EmptyState>
                Nenhum pesquisador encontrado para esse tema. Tente outra palavra-chave.
              </EmptyState>
            )}
          </>
        )}

        {!hasSearched && !isLoading && !errorMessage && (
          <StateMessage>
            Digite um tema de pesquisa acima e clique em "Buscar" para encontrar autores.
          </StateMessage>
        )}
      </PageContent>
    </Page>
  );
};

export default ResearcherSearch;
