import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { motion } from 'framer-motion';

export default function MetricCard({ icon: Icon, title, value, subtitle }) {
  return (
    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
      <Card sx={{ display: 'flex', alignItems: 'center', p: 2, borderRadius: 2, boxShadow: 3 }}>
        {Icon && (
          <Box sx={{ mr: 2 }}>
            <Icon fontSize="large" />
          </Box>
        )}
        <CardContent sx={{ flex: 1 }}>
          <Typography variant="h6">{title}</Typography>
          <Typography variant="h4">{value}</Typography>
          {subtitle && <Typography variant="body2" color="textSecondary">{subtitle}</Typography>}
        </CardContent>
      </Card>
    </motion.div>
  );
}
