#!/bin/bash
ln -sf /opt/node_app/node_modules/* ./node_modules/.
cp src/configs/local.js src/configs/configs.js
gatsby develop --host 0.0.0.0
