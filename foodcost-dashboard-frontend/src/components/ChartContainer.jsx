import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { motion } from 'framer-motion';

export default function ChartContainer({ title, children }) {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
      <Card sx={{ p: 2, borderRadius: 2, boxShadow: 2 }}>
        {title && <Typography variant="h6" gutterBottom>{title}</Typography>}
        <CardContent>{children}</CardContent>
      </Card>
    </motion.div>
  );
}
