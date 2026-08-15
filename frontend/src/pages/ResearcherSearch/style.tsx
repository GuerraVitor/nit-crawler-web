import styled from "styled-components";
import { motion } from "framer-motion";
import { Input, Button } from "antd";

export const Page = styled(motion.div)`
  min-height: 100%;
  background: radial-gradient(1200px circle at 0% 0%, #eef5ff 0%, #f7f9fc 45%, #ffffff 100%);
  padding: 2.5rem 1.5rem 3rem;
`;

export const PageContent = styled.div`
  max-width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
`;

export const Hero = styled.div`
  background: linear-gradient(120deg, rgba(0, 95, 75, 0.08), rgba(0, 95, 75, 0.02));
  border: 1px solid rgba(0, 95, 75, 0.12);
  border-radius: 18px;
  padding: 2rem 2.25rem;
`;

export const HeroTitle = styled.h1`
  margin: 0 0 0.5rem;
  font-size: 2.4rem;
  letter-spacing: -0.02em;
`;

export const HeroSubtitle = styled.p`
  margin: 0;
  max-width: 640px;
  color: #55616e;
  font-size: 1.05rem;
`;

export const SearchPanel = styled.form`
  background: #ffffff;
  border: 1px solid #e3e9f0;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
  display: flex;
  gap: 0.75rem;

  @media (max-width: 640px) {
    flex-direction: column;
  }
`;

export const SearchInput = styled(Input)`
  height: 46px;
  font-size: 1rem;
  border-radius: 10px;
`;

export const SearchButton = styled(Button)`
  height: 46px;
  padding: 0 1.75rem;
  border-radius: 10px;
  font-weight: 600;
  background: linear-gradient(120deg, var(--primary-green), #0c7a61);
  border: none;

  &:hover,
  &:focus {
    background: var(--primary-green-darker) !important;
  }
`;

export const ResultsHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
`;

export const ResultsTitle = styled.h2`
  margin: 0;
  font-size: 1.5rem;
`;

export const ResultsCount = styled.span`
  background: #eef3f8;
  color: #3a4654;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 600;
`;

export const StateMessage = styled(motion.p)`
  background: #f7f9fc;
  border: 1px dashed #d6dee8;
  color: #5b6776;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
`;

export const EmptyState = styled(motion.p)`
  background: #fff8f2;
  border: 1px dashed #f2c9a6;
  color: #8a5a2d;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
`;

export const ErrorState = styled(motion.p)`
  background: #fdf2f2;
  border: 1px dashed #e6a3a3;
  color: #9c3b3b;
  padding: 1.25rem 1.5rem;
  border-radius: 12px;
`;
