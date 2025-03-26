-- 创建教师用户注册触发器
DELIMITER //

CREATE TRIGGER after_user_insert
AFTER INSERT ON api_user
FOR EACH ROW
BEGIN
    -- 只处理教师用户
    IF NEW.role = 'teacher' THEN
        -- 插入staff记录
        INSERT INTO api_staff (user_id, position)
        VALUES (NEW.id, 'teacher');
        
        -- 获取刚插入的staff记录ID
        SET @staff_id = LAST_INSERT_ID();
        
        -- 插入classteacher记录
        INSERT INTO api_classteacher (teacher_id, assigned_at)
        VALUES (@staff_id, NOW());
    END IF;
END//

DELIMITER ;

-- 删除触发器的语句（备用）
DROP TRIGGER IF EXISTS after_user_insert;