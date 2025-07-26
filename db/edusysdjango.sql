/*
 Navicat Premium Dump SQL

 Source Server         : test1
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42)
 Source Host           : localhost:3306
 Source Schema         : edusysdjango

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42)
 File Encoding         : 65001

 Date: 26/07/2025 09:50:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 73 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add books', 7, 'add_books');
INSERT INTO `auth_permission` VALUES (26, 'Can change books', 7, 'change_books');
INSERT INTO `auth_permission` VALUES (27, 'Can delete books', 7, 'delete_books');
INSERT INTO `auth_permission` VALUES (28, 'Can view books', 7, 'view_books');
INSERT INTO `auth_permission` VALUES (29, 'Can add student', 8, 'add_student');
INSERT INTO `auth_permission` VALUES (30, 'Can change student', 8, 'change_student');
INSERT INTO `auth_permission` VALUES (31, 'Can delete student', 8, 'delete_student');
INSERT INTO `auth_permission` VALUES (32, 'Can view student', 8, 'view_student');
INSERT INTO `auth_permission` VALUES (33, 'Can add document submission', 9, 'add_documentsubmission');
INSERT INTO `auth_permission` VALUES (34, 'Can change document submission', 9, 'change_documentsubmission');
INSERT INTO `auth_permission` VALUES (35, 'Can delete document submission', 9, 'delete_documentsubmission');
INSERT INTO `auth_permission` VALUES (36, 'Can view document submission', 9, 'view_documentsubmission');
INSERT INTO `auth_permission` VALUES (37, 'Can add 写作题目', 10, 'add_writingtopic');
INSERT INTO `auth_permission` VALUES (38, 'Can change 写作题目', 10, 'change_writingtopic');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 写作题目', 10, 'delete_writingtopic');
INSERT INTO `auth_permission` VALUES (40, 'Can view 写作题目', 10, 'view_writingtopic');
INSERT INTO `auth_permission` VALUES (41, 'Can add 学生', 11, 'add_student');
INSERT INTO `auth_permission` VALUES (42, 'Can change 学生', 11, 'change_student');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 学生', 11, 'delete_student');
INSERT INTO `auth_permission` VALUES (44, 'Can view 学生', 11, 'view_student');
INSERT INTO `auth_permission` VALUES (45, 'Can add 题目文档提交', 12, 'add_submission');
INSERT INTO `auth_permission` VALUES (46, 'Can change 题目文档提交', 12, 'change_submission');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 题目文档提交', 12, 'delete_submission');
INSERT INTO `auth_permission` VALUES (48, 'Can view 题目文档提交', 12, 'view_submission');
INSERT INTO `auth_permission` VALUES (49, 'Can add 班级', 13, 'add_class');
INSERT INTO `auth_permission` VALUES (50, 'Can change 班级', 13, 'change_class');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 班级', 13, 'delete_class');
INSERT INTO `auth_permission` VALUES (52, 'Can view 班级', 13, 'view_class');
INSERT INTO `auth_permission` VALUES (53, 'Can add 课程', 14, 'add_course');
INSERT INTO `auth_permission` VALUES (54, 'Can change 课程', 14, 'change_course');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 课程', 14, 'delete_course');
INSERT INTO `auth_permission` VALUES (56, 'Can view 课程', 14, 'view_course');
INSERT INTO `auth_permission` VALUES (57, 'Can add 课程资源', 15, 'add_courseresource');
INSERT INTO `auth_permission` VALUES (58, 'Can change 课程资源', 15, 'change_courseresource');
INSERT INTO `auth_permission` VALUES (59, 'Can delete 课程资源', 15, 'delete_courseresource');
INSERT INTO `auth_permission` VALUES (60, 'Can view 课程资源', 15, 'view_courseresource');
INSERT INTO `auth_permission` VALUES (61, 'Can add 作业', 16, 'add_homework');
INSERT INTO `auth_permission` VALUES (62, 'Can change 作业', 16, 'change_homework');
INSERT INTO `auth_permission` VALUES (63, 'Can delete 作业', 16, 'delete_homework');
INSERT INTO `auth_permission` VALUES (64, 'Can view 作业', 16, 'view_homework');
INSERT INTO `auth_permission` VALUES (65, 'Can add 教师', 17, 'add_teacher');
INSERT INTO `auth_permission` VALUES (66, 'Can change 教师', 17, 'change_teacher');
INSERT INTO `auth_permission` VALUES (67, 'Can delete 教师', 17, 'delete_teacher');
INSERT INTO `auth_permission` VALUES (68, 'Can view 教师', 17, 'view_teacher');
INSERT INTO `auth_permission` VALUES (69, 'Can add 班级课程选修', 18, 'add_courseenrollment');
INSERT INTO `auth_permission` VALUES (70, 'Can change 班级课程选修', 18, 'change_courseenrollment');
INSERT INTO `auth_permission` VALUES (71, 'Can delete 班级课程选修', 18, 'delete_courseenrollment');
INSERT INTO `auth_permission` VALUES (72, 'Can view 班级课程选修', 18, 'view_courseenrollment');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$1000000$ih62emyzHUUDM8uTK0B4C4$6lv/ojkJX2Rz7Be/t2OX1B9FmXteVZt6NfA3yIfM1y0=', '2025-07-23 08:52:42.459472', 0, 'student004', '', '', 'student001@example.com', 0, 1, '2025-07-23 08:52:36.026895');
INSERT INTO `auth_user` VALUES (2, 'pbkdf2_sha256$1000000$keXjffEkXIZHVbE5Z1ebiy$DR/Z0lShQqATJRpG7621WOxamtm3yfqJBrCXUyqpOVU=', NULL, 0, 'student003', '', '', '', 0, 1, '2025-07-23 09:40:10.119107');
INSERT INTO `auth_user` VALUES (3, 'pbkdf2_sha256$1000000$9vV7E7nkQfEX1j4vKOs9Mf$t2IMK7piwSjtOMvGeUB2jQyE/2Gu/+vLuAdUT99VXy8=', NULL, 0, 'student005', '', '', 'student001@example.com', 0, 1, '2025-07-23 12:47:20.009959');
INSERT INTO `auth_user` VALUES (4, 'pbkdf2_sha256$1000000$Ysd74Ibjf3qWtMtK4Dl00w$kk0okO0xxVGXp/n2iMHoMIflzU8/aXmTXEMfH6xvNJQ=', NULL, 0, 'student006', '', '', 'student001@example.com', 0, 1, '2025-07-24 03:13:06.738231');
INSERT INTO `auth_user` VALUES (7, 'pbkdf2_sha256$1000000$6cHcIbPoubYWAO4raQZvf8$4W1Vy+8DJea8Rdom/Y3P7nMnFJvLi30PHOirnvVjLHc=', NULL, 0, 'teacher003', '', '', 'zhang@example.com', 0, 1, '2025-07-24 09:22:46.261436');
INSERT INTO `auth_user` VALUES (8, 'pbkdf2_sha256$1000000$YaP1jktUOn5H6AdVTtahlC$h1rt5W/ox9sBBM3KjPl5/QS8ASQnrMc6lOEj7lvqWbA=', NULL, 0, 'teacher005', '', '', 'zhang@example.com', 0, 1, '2025-07-24 12:18:50.133699');

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (7, 'goods', 'books');
INSERT INTO `django_content_type` VALUES (9, 'goods', 'documentsubmission');
INSERT INTO `django_content_type` VALUES (8, 'goods', 'student');
INSERT INTO `django_content_type` VALUES (10, 'goods', 'writingtopic');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (11, 'students', 'student');
INSERT INTO `django_content_type` VALUES (12, 'students', 'submission');
INSERT INTO `django_content_type` VALUES (13, 'teachers', 'class');
INSERT INTO `django_content_type` VALUES (14, 'teachers', 'course');
INSERT INTO `django_content_type` VALUES (18, 'teachers', 'courseenrollment');
INSERT INTO `django_content_type` VALUES (15, 'teachers', 'courseresource');
INSERT INTO `django_content_type` VALUES (16, 'teachers', 'homework');
INSERT INTO `django_content_type` VALUES (17, 'teachers', 'teacher');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 67 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-07-23 02:38:19.655147');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-07-23 02:38:20.700881');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-07-23 02:38:20.898835');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-07-23 02:38:20.908646');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-23 02:38:20.916763');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-07-23 02:38:21.061372');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-07-23 02:38:21.158774');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-07-23 02:38:21.181726');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-07-23 02:38:21.189172');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-07-23 02:38:21.262529');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-07-23 02:38:21.268539');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-07-23 02:38:21.277729');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-07-23 02:38:21.375613');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-07-23 02:38:21.465641');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-07-23 02:38:21.484653');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-07-23 02:38:21.491703');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-07-23 02:38:21.584718');
INSERT INTO `django_migrations` VALUES (18, 'goods', '0001_initial', '2025-07-23 02:38:21.623674');
INSERT INTO `django_migrations` VALUES (19, 'goods', '0002_rename_book_goods', '2025-07-23 02:38:21.655297');
INSERT INTO `django_migrations` VALUES (20, 'goods', '0003_rename_goods_books', '2025-07-23 02:38:21.686213');
INSERT INTO `django_migrations` VALUES (21, 'goods', '0004_student', '2025-07-23 02:38:21.719776');
INSERT INTO `django_migrations` VALUES (22, 'goods', '0005_alter_student_rdate', '2025-07-23 02:38:21.727285');
INSERT INTO `django_migrations` VALUES (23, 'goods', '0006_alter_student_age_alter_student_is_available_and_more', '2025-07-23 02:38:21.958342');
INSERT INTO `django_migrations` VALUES (24, 'goods', '0007_alter_student_sex', '2025-07-23 02:38:22.103412');
INSERT INTO `django_migrations` VALUES (25, 'goods', '0008_alter_student_level_alter_student_sex', '2025-07-23 02:38:22.237720');
INSERT INTO `django_migrations` VALUES (26, 'goods', '0009_alter_student_sex', '2025-07-23 02:38:22.255341');
INSERT INTO `django_migrations` VALUES (27, 'goods', '0010_remove_student_sex', '2025-07-23 02:38:22.316489');
INSERT INTO `django_migrations` VALUES (28, 'goods', '0011_auto_20250719_2109', '2025-07-23 02:38:22.323000');
INSERT INTO `django_migrations` VALUES (29, 'goods', '0012_auto_20250719_2117', '2025-07-23 02:38:22.328638');
INSERT INTO `django_migrations` VALUES (30, 'goods', '0013_student_sex', '2025-07-23 02:38:22.400949');
INSERT INTO `django_migrations` VALUES (31, 'goods', '0014_student_is_active_student_jwt', '2025-07-23 02:38:22.524664');
INSERT INTO `django_migrations` VALUES (32, 'goods', '0015_documentsubmission', '2025-07-23 02:38:22.561197');
INSERT INTO `django_migrations` VALUES (33, 'goods', '0016_student_user', '2025-07-23 02:38:22.658681');
INSERT INTO `django_migrations` VALUES (34, 'goods', '0017_writingtopic', '2025-07-23 02:38:22.701519');
INSERT INTO `django_migrations` VALUES (35, 'goods', '0018_remove_writingtopic_d_path_and_more', '2025-07-23 02:38:22.964882');
INSERT INTO `django_migrations` VALUES (36, 'goods', '0019_documentsubmission_filename_documentsubmission_path', '2025-07-23 02:38:23.114331');
INSERT INTO `django_migrations` VALUES (37, 'sessions', '0001_initial', '2025-07-23 02:38:23.177315');
INSERT INTO `django_migrations` VALUES (38, 'students', '0001_initial', '2025-07-23 02:38:23.256142');
INSERT INTO `django_migrations` VALUES (39, 'students', '0002_alter_student_s_num_alter_submission_u_num', '2025-07-23 02:38:23.263647');
INSERT INTO `django_migrations` VALUES (40, 'students', '0003_alter_student_s_num_alter_submission_u_num', '2025-07-23 02:38:23.271680');
INSERT INTO `django_migrations` VALUES (41, 'teachers', '0001_initial', '2025-07-23 02:38:23.480305');
INSERT INTO `django_migrations` VALUES (42, 'teachers', '0002_alter_class_c_num_alter_course_credit_and_more', '2025-07-23 02:38:23.494209');
INSERT INTO `django_migrations` VALUES (43, 'teachers', '0003_alter_class_c_num_alter_class_number_and_more', '2025-07-23 02:38:23.503379');
INSERT INTO `django_migrations` VALUES (44, 'students', '0004_alter_student_password_alter_student_s_num_and_more', '2025-07-23 04:00:54.947226');
INSERT INTO `django_migrations` VALUES (45, 'teachers', '0004_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 04:00:55.215050');
INSERT INTO `django_migrations` VALUES (46, 'students', '0005_alter_student_class_name_alter_student_email_and_more', '2025-07-23 04:03:47.003876');
INSERT INTO `django_migrations` VALUES (47, 'teachers', '0005_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 04:03:47.089444');
INSERT INTO `django_migrations` VALUES (48, 'students', '0006_alter_student_s_num_alter_submission_u_num', '2025-07-23 04:10:53.649206');
INSERT INTO `django_migrations` VALUES (49, 'teachers', '0006_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 04:10:53.659207');
INSERT INTO `django_migrations` VALUES (50, 'goods', '0020_remove_student_user', '2025-07-23 08:33:32.844512');
INSERT INTO `django_migrations` VALUES (51, 'students', '0007_student_user_alter_student_s_num_and_more', '2025-07-23 08:33:32.995956');
INSERT INTO `django_migrations` VALUES (52, 'teachers', '0007_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 08:33:33.006957');
INSERT INTO `django_migrations` VALUES (53, 'students', '0008_alter_submission_u_num', '2025-07-23 09:40:02.402255');
INSERT INTO `django_migrations` VALUES (54, 'teachers', '0008_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 09:40:02.411289');
INSERT INTO `django_migrations` VALUES (55, 'students', '0009_alter_student_jwt_alter_submission_u_num', '2025-07-23 13:16:27.986813');
INSERT INTO `django_migrations` VALUES (56, 'teachers', '0009_alter_class_c_num_alter_course_l_num_and_more', '2025-07-23 13:16:27.995876');
INSERT INTO `django_migrations` VALUES (57, 'students', '0010_remove_student_class_name_student_class_num_and_more', '2025-07-24 08:23:16.436971');
INSERT INTO `django_migrations` VALUES (58, 'teachers', '0010_alter_class_c_num_alter_course_l_num_and_more', '2025-07-24 08:23:16.444015');
INSERT INTO `django_migrations` VALUES (59, 'students', '0011_alter_submission_u_num', '2025-07-24 09:11:23.271205');
INSERT INTO `django_migrations` VALUES (60, 'teachers', '0011_teacher_user_alter_class_c_num_alter_course_l_num_and_more', '2025-07-24 09:11:23.376429');
INSERT INTO `django_migrations` VALUES (61, 'students', '0012_alter_submission_u_num', '2025-07-24 09:30:49.868664');
INSERT INTO `django_migrations` VALUES (62, 'teachers', '0012_alter_class_c_num_alter_course_l_num_and_more', '2025-07-24 09:30:49.972520');
INSERT INTO `django_migrations` VALUES (63, 'students', '0013_alter_submission_u_num', '2025-07-24 09:53:29.101697');
INSERT INTO `django_migrations` VALUES (64, 'teachers', '0013_alter_class_c_num_alter_course_l_num_and_more', '2025-07-24 09:53:29.113346');
INSERT INTO `django_migrations` VALUES (65, 'students', '0014_alter_submission_u_num', '2025-07-24 10:24:50.425732');
INSERT INTO `django_migrations` VALUES (66, 'teachers', '0014_alter_course_l_num_alter_courseenrollment_o_num_and_more', '2025-07-24 10:24:50.438239');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('00fcwxng80szpukvw2t4tduztkonr5g1', '.eJxVjMsOwiAQRf-FtSEMjym4dO83EGBAqgaS0q6M_65NutDtPefcF_NhW6vfRl78TOzMgJ1-txjSI7cd0D20W-ept3WZI98VftDBr53y83K4fwc1jPqt5WRMyAgCQKJxKltXcgJFLhSNk0FFVgqrVUkJoi6AxpJxgBodaeHY-wO3wTaa:1ueVDO:GpzFVJZB8vDH-BSC-Tqhi1BAPXrtVHGv7Urpofk9r68', '2025-08-06 08:52:42.466472');
INSERT INTO `django_session` VALUES ('9c4djni9ecrz908rb7plmof7sh30bao2', 'e30:1ueV6t:yisBFHeCCttxmBz0wN9QWUkabmOik82CazPfsjplMYQ', '2025-08-06 08:45:59.597687');
INSERT INTO `django_session` VALUES ('u9hfjd9jo8ztyhya7r19ti28jcq6udi9', 'e30:1ueV3z:MHuYNeOCwTvYkpO7p-f6xzqyrux9R_Fw4s5Ki-AM-4Q', '2025-08-06 08:42:59.576236');

-- ----------------------------
-- Table structure for goods_books
-- ----------------------------
DROP TABLE IF EXISTS `goods_books`;
CREATE TABLE `goods_books`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `price` double NOT NULL,
  `description` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_books
-- ----------------------------

-- ----------------------------
-- Table structure for goods_documentsubmission
-- ----------------------------
DROP TABLE IF EXISTS `goods_documentsubmission`;
CREATE TABLE `goods_documentsubmission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `u_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `s_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `t_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `up_time` datetime(6) NULL DEFAULT NULL,
  `score` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `advice` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `ressuggest` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `knowledgegraph` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `path` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_documentsubmission
-- ----------------------------

-- ----------------------------
-- Table structure for goods_student
-- ----------------------------
DROP TABLE IF EXISTS `goods_student`;
CREATE TABLE `goods_student`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `age` int NULL DEFAULT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `snum` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `rdate` date NOT NULL,
  `lastlogin` datetime(6) NULL DEFAULT NULL,
  `is_available` tinyint(1) NULL DEFAULT NULL,
  `level` int NULL DEFAULT NULL,
  `sex` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  `jwt` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_student
-- ----------------------------

-- ----------------------------
-- Table structure for goods_writingtopic
-- ----------------------------
DROP TABLE IF EXISTS `goods_writingtopic`;
CREATE TABLE `goods_writingtopic`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `des` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `types` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of goods_writingtopic
-- ----------------------------

-- ----------------------------
-- Table structure for students_student
-- ----------------------------
DROP TABLE IF EXISTS `students_student`;
CREATE TABLE `students_student`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `s_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `jwt` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `createtime` datetime(6) NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  `class_num` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `students_student_s_num_31bb410a_uniq`(`s_num` ASC) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `students_student_user_id_56286dbb_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of students_student
-- ----------------------------
INSERT INTO `students_student` VALUES (1, '7325e0c8', '张三', 'student001', 'pbkdf2_sha256$1000000$I7srhOUPWO01iv9XnxNiHE$jCekegKxBFMYo/qz3jIX48mm/VKEOHAVdTT4XU5qSck=', '13800138000', 'student001@example.com', NULL, '2025-07-23 04:03:51.833279', NULL, NULL);
INSERT INTO `students_student` VALUES (2, '2025072300002', '张三', 'student002', 'pbkdf2_sha256$1000000$1dGdlfCK94HzKPpHXxV8QD$QDp4cjbnY+ncRq2VuSr3Krdu8TYCKdQMIo/oZMR/EPA=', '13800138000', 'student001@example.com', NULL, '2025-07-23 04:11:08.447446', NULL, NULL);
INSERT INTO `students_student` VALUES (3, '2025072300003', '张三', 'student003', 'pbkdf2_sha256$1000000$rtARnQ3hWJpeOJnsC5WXjm$dOEBuquIsI04A4xtd+IOn5p4e0p+gDxg1QOexjDivZw=', '13800138000', 'student001@example.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzMjc2NjEzLCJpYXQiOjE3NTMyNzQ4MTMsImp0aSI6IjJjYWI2YzkyMjEyYzQxNmZhNTFkYmUwYzAzZTJlMDEwIiwidXNlcl9pZCI6IjIifQ.yiLocm9bfCc80MKnKAl13tXx9a4iyqDHn3TfoWtwZB0', '2025-07-23 04:11:14.031671', 2, NULL);
INSERT INTO `students_student` VALUES (4, '2025072300004', '张三', 'student004', 'pbkdf2_sha256$1000000$oNrr94674hn8XLBi4zQEJa$EcZhb2WHEw/pXbq5n9CP2hb3t7ccu0qAQG2DxqeVHsY=', '13800138000', 'student001@example.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUzMjY1MDE2LCJpYXQiOjE3NTMyNjMyMTYsImp0aSI6IjI0NzAyZmU1ZjEzODQ1NjhhMWM0MWY4N2U3YTFmZjllIiwidXNlcl9pZCI6IjEifQ.57UGJhERRYIY4WQF_YP3s-D-a1FAazvY-dsxIrFDFnM', '2025-07-23 08:52:36.886253', 1, NULL);
INSERT INTO `students_student` VALUES (5, '2025072300005', '张三', 'student005', 'pbkdf2_sha256$1000000$4r3wRPYxGoiG071SiqD1eK$bz+nU5ckqoDvXARGLBviI/It8Xkpk2uZ/8e38mY+cWU=', '13800138000', 'student001@example.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MzQxMzE3NywiaWF0IjoxNzUzMzI2Nzc3LCJqdGkiOiI1OTA5NjNkN2M0ZDE0NWFkOWFlMDM0OTAyYWNlNjQ0MiIsInVzZXJfaWQiOjUsInVzZXJuYW1lIjoic3R1ZGVudDAwNSIsInVzZXJfdHlwZSI6InN0dWRlbnQiLCJudW0iOiIyMDI1MDcyMzAwMDA1In0.xEQqupsLmaPjMhjcb5dWSzeBeWlSDVwdoKOQFLfpwcA', '2025-07-23 12:47:20.579108', 3, NULL);
INSERT INTO `students_student` VALUES (6, '2025072400001', '张三', 'lijunze_new', 'pbkdf2_sha256$1000000$1BmFyilsCN71anw6GHEOl4$wK9YcoOBLxcP5BIxXg4dlkOo4KsJLBu6soq4SIBAD3w=', '13987654321', 'lijunze_new@example.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MzQzMjQ5OSwiaWF0IjoxNzUzMzQ2MDk5LCJqdGkiOiJkZmM4ZDYxZmQzNjU0MWM0YmExZWExZWI2ZDk1MWNkYyIsInVzZXJfaWQiOjYsInVzZXJuYW1lIjoic3R1ZGVudDAwNiIsInVzZXJfdHlwZSI6InN0dWRlbnQiLCJudW0iOiIyMDI1MDcyNDAwMDAxIn0.3yv6iNVKWQ_fY-ewEL8-3SYcys9I-B6lXvUKBB4OfMI', '2025-07-24 03:13:07.381031', 4, NULL);

-- ----------------------------
-- Table structure for students_submission
-- ----------------------------
DROP TABLE IF EXISTS `students_submission`;
CREATE TABLE `students_submission`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `u_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `s_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `h_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `up_time` datetime(6) NULL DEFAULT NULL,
  `score` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `advice` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `ressuggest` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `knowledgegraph` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `status` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of students_submission
-- ----------------------------

-- ----------------------------
-- Table structure for teachers_class
-- ----------------------------
DROP TABLE IF EXISTS `teachers_class`;
CREATE TABLE `teachers_class`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `c_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `c_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `t_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `grade` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `number` int NULL DEFAULT NULL,
  `createtime` datetime(6) NOT NULL,
  `updatetime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_class
-- ----------------------------
INSERT INTO `teachers_class` VALUES (1, '2025072400001', '高级Python班', '2025072400001', '2023级', 45, '2025-07-24 10:07:36.756524', '2025-07-24 12:32:41.068448');
INSERT INTO `teachers_class` VALUES (2, '2025072400002', '2023级计算机科学与技术1班', '2025072400001', '2023', 0, '2025-07-24 12:23:49.377077', '2025-07-24 12:23:49.378077');

-- ----------------------------
-- Table structure for teachers_course
-- ----------------------------
DROP TABLE IF EXISTS `teachers_course`;
CREATE TABLE `teachers_course`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `l_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `t_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `des` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `type` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `credit` int NULL DEFAULT NULL,
  `createtime` datetime(6) NOT NULL,
  `updatetime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_course
-- ----------------------------
INSERT INTO `teachers_course` VALUES (1, '870b51f5', '高级人工智能', '2025072400001', '本课程介绍人工智能的前沿技术和应用', '专业选修课', 3, '2025-07-24 10:23:23.736530', '2025-07-24 10:23:23.736530');
INSERT INTO `teachers_course` VALUES (2, 'ac1879f1', '高级人工智能2', '2025072400001', '本课程介绍人工智能的前沿技术和应用', '专业选修课', 3, '2025-07-24 10:24:59.853307', '2025-07-24 10:24:59.853307');
INSERT INTO `teachers_course` VALUES (3, '2025072400003', '高级人工智能导论77', '2025072400001', '本课程系统介绍人工智能的基础理论与前沿技术应用', '专业必修课', 4, '2025-07-24 10:25:27.001103', '2025-07-24 12:30:11.389379');
INSERT INTO `teachers_course` VALUES (4, '2025072400004', '高级人工智能4', '2025072400001', '本课程介绍人工智能的前沿技术和应用', '专业选修课', 3, '2025-07-24 12:26:45.747470', '2025-07-24 12:26:45.747470');

-- ----------------------------
-- Table structure for teachers_courseenrollment
-- ----------------------------
DROP TABLE IF EXISTS `teachers_courseenrollment`;
CREATE TABLE `teachers_courseenrollment`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `o_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `c_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `l_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `createtime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `teachers_courseenrollment_c_num_l_num_57b28dce_uniq`(`c_num` ASC, `l_num` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_courseenrollment
-- ----------------------------
INSERT INTO `teachers_courseenrollment` VALUES (1, 'CE2025072400001', '2025072400001', '2025072400003', '2025-07-24 12:01:04.181647');

-- ----------------------------
-- Table structure for teachers_courseresource
-- ----------------------------
DROP TABLE IF EXISTS `teachers_courseresource`;
CREATE TABLE `teachers_courseresource`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `r_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `l_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `r_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `r_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `r_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `createtime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_courseresource
-- ----------------------------

-- ----------------------------
-- Table structure for teachers_homework
-- ----------------------------
DROP TABLE IF EXISTS `teachers_homework`;
CREATE TABLE `teachers_homework`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `h_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `l_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `title` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `des` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `hd_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `hd_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `hd_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `createtime` datetime(6) NOT NULL,
  `updatetime` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_homework
-- ----------------------------

-- ----------------------------
-- Table structure for teachers_teacher
-- ----------------------------
DROP TABLE IF EXISTS `teachers_teacher`;
CREATE TABLE `teachers_teacher`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `t_num` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `jwt` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `createtime` datetime(6) NOT NULL,
  `user_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `teachers_teacher_user_id_cdea3fc2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of teachers_teacher
-- ----------------------------
INSERT INTO `teachers_teacher` VALUES (1, '2025072400001', '张教授更新', 'teacher0006', 'pbkdf2_sha256$1000000$lSR2XPaEOsLwyz1Ly4OjkT$KgyOLF5xlGWXehRFAL+ZOFYvthIq8kHMXyOWrk/2TaA=', '13900139000', 'zhang_update@example.com', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1MzQ0NTc5MywiaWF0IjoxNzUzMzU5MzkzLCJqdGkiOiJkM2JiYzFjYjQyMTA0MWNhYTljZWRhZWVjYmI0YTcyYSIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoidGVhY2hlcjAwMyIsInVzZXJfdHlwZSI6InRlYWNoZXIiLCJudW0iOiIyMDI1MDcyNDAwMDAxIn0.oRkRS-YZP3vxAxRje3csk6WkGZ72hcnoYZn5PWBu1Wg', '2025-07-24 09:22:46.860477', 7);
INSERT INTO `teachers_teacher` VALUES (2, '2025072400002', '张教授', 'teacher005', 'pbkdf2_sha256$1000000$GgeFLPOpbEBsc0p5c9fEhX$Em64WEWskdMm/RmYoYGKyHW9DnhtEwsg81pmPLPwsfU=', '13800138000', 'zhang@example.com', NULL, '2025-07-24 12:18:50.946210', 8);

SET FOREIGN_KEY_CHECKS = 1;
