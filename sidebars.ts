// ...existing code...
import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: 'The Physical Human Robotic AI',
      link: {
        type: 'generated-index',
        title: 'Physical Human Robotic AI',
        description: 'Learn about the core concepts of Physical Human Robotic AI.',
        slug: '/the-physical-human-robotic-ai',
      },
      items: [
        'The Physical Human Robotic AI/index',
        {
          type: 'category',
          label: 'Chapter-2: ROS 2 Fundamentals',
          link: {
            type: 'doc',
            id: 'The Physical Human Robotic AI/Chapter-2/index',
          },
          items: [
            'The Physical Human Robotic AI/Chapter-2/what-is-ros2',
            'The Physical Human Robotic AI/Chapter-2/nodes',
            'The Physical Human Robotic AI/Chapter-2/topics',
            'The Physical Human Robotic AI/Chapter-2/services',
            'The Physical Human Robotic AI/Chapter-2/actions',
            'The Physical Human Robotic AI/Chapter-2/parameters',
            'The Physical Human Robotic AI/Chapter-2/launch-files',
            'The Physical Human Robotic AI/Chapter-2/messages-services',
            'The Physical Human Robotic AI/Chapter-2/debugging',
            'The Physical Human Robotic AI/Chapter-2/logging-lifecycle',
            'The Physical Human Robotic AI/Chapter-2/urdf',
            'The Physical Human Robotic AI/Chapter-2/visualization',
            'The Physical Human Robotic AI/Chapter-2/time',
            'The Physical Human Robotic AI/Chapter-2/architecture',
            'The Physical Human Robotic AI/Chapter-2/sensor-drivers',
            'The Physical Human Robotic AI/Chapter-2/motor-controllers',
            'The Physical Human Robotic AI/Chapter-2/capstone-preview',
            'The Physical Human Robotic AI/Chapter-2/environment',
          ],
        },
        // Placeholder for other chapters
        // 'The Physical Human Robotic AI/Chapter-1', // Placeholder
        // 'The Physical Human Robotic AI/Chapter-3', // Placeholder
        // 'The Physical Human Robotic AI/Chapter-4', // Placeholder
        // 'The Physical Human Robotic AI/Chapter-5', // Placeholder
      ],
    },
    'intro', // Keep existing intro, but it might be deleted later
  ],

  // But you can create a sidebar manually
  /*
  tutorialSidebar: [
    'intro',
    'hello',
    {
      type: 'category',
      label: 'Tutorial',
      items: ['tutorial-basics/create-a-document'],
    },
  ],
   */
};

export default sidebars;
// ...existing code...