import React from 'react';
import { Box, Typography, Accordion, AccordionSummary, AccordionDetails, useTheme } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';

const faqItems = [
  {
    question: 'Cos\u2019\u00e8 DataDash?',
    answer: 'DataDash \u00e8 una piattaforma di analisi per la ristorazione che ti aiuta a ottimizzare costi, inventario e performance.',
  },
  {
    question: 'Quanto costa DataDash?',
    answer: 'Offriamo un mese di prova gratuito; successivamente puoi scegliere piani mensili o annuali in base alle tue esigenze.',
  },
  {
    question: 'Come posso iniziare?',
    answer: 'Registrati e inizia subito la tua prova gratuita senza inserire dati di pagamento.',
  },
  {
    question: 'Come funziona la cancellazione?',
    answer: 'Puoi disdire in qualsiasi momento dal tuo account senza costi aggiuntivi.',
  },
  {
    question: 'Quali metriche posso monitorare?',
    answer: 'Vendite per prodotto, food cost, margine lordo, scorte di magazzino e performance rider.',
  },
  {
    question: 'DataDash \u00e8 adatto ai piccoli ristoranti?',
    answer: 'S\u00ec, l\u2019MVP è pensato per uso locale con zero costi fissi, ideale per piccoli esercizi.',
  },
];

export default function FAQ() {
  const theme = useTheme();

  return (
    <Box sx={{ width: '80%', margin: '0 auto', mt: 8, mb: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 3, color: '#fff' }}>
        FAQ - Domande Frequenti
      </Typography>

      {faqItems.map((item, index) => (
        <Accordion
          key={index}
          sx={{
            backgroundColor: theme.palette.mode === 'dark' ? '#333' : '#f5f5f5',
            color: theme.palette.getContrastText(theme.palette.background.paper),
            mb: 1,
          }}
        >
          <AccordionSummary
            expandIcon={<AddIcon sx={{ color: '#fff' }} />}
            sx={{
              '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded': {
                transform: 'rotate(45deg)',
              },
              '& .MuiAccordionSummary-expandIconWrapper.Mui-expanded > svg': {
                color: '#fff',
              },
            }}
          >
            <Typography sx={{ fontWeight: 600 }}>{item.question}</Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography>{item.answer}</Typography>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );
}
