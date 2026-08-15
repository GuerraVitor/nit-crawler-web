import styled from "styled-components";

export const CardContainer = styled.div`
  background-color: var(--card-background);
  border: 1px solid #e1e7ef;
  border-radius: 16px;
  padding: 1.75rem;
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;

  &:hover {
    border-color: #c6d2e1;
    transform: translateY(-2px);
    box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
  }
`;

export const CardHeader = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 0.75rem;
`;

export const CardTitle = styled.h3`
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-color);
`;

export const CardSubtitle = styled.p`
  margin: 0;
  font-size: 0.92rem;
  color: #6c7a89;
`;

export const InterestsRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.9rem 0 1.25rem;
`;

export const InterestPill = styled.span<{ $matched?: boolean }>`
  background: ${({ $matched }) => ($matched ? "#e6f5f1" : "#eef3f8")};
  color: ${({ $matched }) => ($matched ? "#0c7a61" : "#2f3b4a")};
  border: 1px solid ${({ $matched }) => ($matched ? "#0c7a61" : "transparent")};
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
`;

export const CardFooter = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
`;

export const FieldLabel = styled.span`
  font-weight: 600;
  color: #6c7a89;
  margin-right: 0.35rem;
`;

export const LattesLink = styled.a`
  display: inline-block;
  background: linear-gradient(120deg, var(--primary-green), #0c7a61);
  color: white;
  padding: 0.55rem 1.2rem;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 20px rgba(0, 95, 75, 0.2);
    color: white;
    text-decoration: none;
  }
`;
